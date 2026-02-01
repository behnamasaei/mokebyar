import asyncio
import pickle

import websockets
import json
import numpy as np
import cv2
import insightface
from insightface.app import FaceAnalysis
import asyncpg  # جایگزین psycopg2 برای سرعت و تزریق همزمانی
import faiss
import os
import base64
import warnings
import ssl
import struct  # برای تبدیل دقیق بایت‌ها (اختیاری ولی تمیزتر)

warnings.filterwarnings("ignore")

# ================= تنظیمات دیتابیس =================
DB_CONFIG = {
    "host": "localhost",
    "database": "mokebyar_db",
    "user": "postgres",
    "password": "root",
    "port": "5432"
}

# ================= تنظیمات SSL =================
CERT_FILE = '../MokebYar/localhost+2.pem'
KEY_FILE = '../MokebYar/localhost+2-key.pem'

INDEX_FILE = "faiss_index.bin"
ID_MAP_FILE = "id_map.pkl"

# پارامترهای بهینه‌سازی
QUALITY_THRESHOLD = 100.0  # آستانه تشخیص تاری (هرچه کمتر، سخت‌گیرانه‌تر)


# ================= کلاس دیتابیس (نسخه Async) =================
class AsyncPostgresFaceDB:
    def __init__(self):
        self.pool = None
    
    async def init_pool(self):
        """ایجاد یک استخر اتصال برای مدیریت همزمانی"""
        try:
            self.pool = await asyncpg.create_pool(**DB_CONFIG, min_size=2, max_size=10)
            async with self.pool.acquire() as conn:
                await conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        embedding BYTEA NOT NULL
                    );
                ''')
            print("✅ DB Pool Ready.")
        except Exception as e:
            print(f"❌ DB Connection Error: {e}")
            exit(1)
    
    async def save_user(self, name, embedding):
        """ذخیره با حذف سربار Pickle و استفاده از بایت خام"""
        # تبدیل مستقیم numpy array به bytes بدون پیکل (حجم کمتر و سرعت بالاتر)
        embedding_bytes = embedding.astype(np.float32).tobytes()
        
        async with self.pool.acquire() as conn:
            try:
                db_id = await conn.fetchval(
                    "INSERT INTO users (name, embedding) VALUES ($1, $2) RETURNING id",
                    name, embedding_bytes
                )
                return db_id
            except Exception as e:
                print(f"DB Save Error: {e}")
                return None
    
    async def get_name_by_id(self, user_id):
        async with self.pool.acquire() as conn:
            name = await conn.fetchval("SELECT name FROM users WHERE id = $1", user_id)
            return name


# ================= کلاس Faiss =================
class FaissSearchEngine:
    def __init__(self):
        self.dimension = 512  # buffalo_l embedding dimension
        self.index = None
        self.id_map = []
        self.load_or_build_index()
    
    def load_or_build_index(self):
        if os.path.exists(INDEX_FILE) and os.path.exists(ID_MAP_FILE):
            print("🚀 Loading Faiss index...")
            self.index = faiss.read_index(INDEX_FILE)
            with open(ID_MAP_FILE, 'rb') as f:
                self.id_map = pickle.load(f)
            print("✅ Index loaded.")
        else:
            print("🔄 Building new Faiss index...")
            # استفاده از Inner Product که برای Cosine Similarity (با نرمال‌سازی) بهینه است
            self.index = faiss.IndexFlatIP(self.dimension)
            self.id_map = []
    
    def add_user(self, db_id, embedding):
        vec = embedding / np.linalg.norm(embedding)
        self.index.add(np.array([vec]).astype('float32'))
        self.id_map.append(db_id)
        self.save_to_disk()
    
    def search(self, embedding, threshold=0.45):  # آستانه کمی تهاجمی‌تر برای کاهش False Positive
        vec = embedding / np.linalg.norm(embedding)
        vec = np.array([vec]).astype('float32')
        
        # جستجو
        k = 1
        distances, indices = self.index.search(vec, k)
        
        if indices[0][0] == -1: return None, None
        
        db_id = self.id_map[indices[0][0]]
        similarity = distances[0][0]  # در اینجا Cosine Similarity است
        
        if similarity > threshold:
            return db_id, similarity
        return None, similarity
    
    def save_to_disk(self):
        faiss.write_index(self.index, INDEX_FILE)
        with open(ID_MAP_FILE, 'wb') as f:
            pickle.dump(self.id_map, f)


# ================= کلاس FaceEngine =================
class FaceEngine:
    def __init__(self):
        print("🤖 Loading buffalo_l model (High Accuracy Mode)...")
        # استفاده از providers=['CPUExecutionProvider'] مناسب برای سرورهای معمولی است
        self.app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        self.app.prepare(ctx_id=-1, det_size=(640, 640))
        print("✅ buffalo_l model loaded.")
    
    def check_blur(self, image):
        """بررسی تاری تصویر با استفاده از Laplacian Variance"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        score = cv2.Laplacian(gray, cv2.CV_64F).var()
        return score > QUALITY_THRESHOLD
    
    def get_embedding_from_image(self, cv2_img):
        if cv2_img is None: return None
        
        # فیلتر کیفیت: اگر تصویر تار باشد، پردازش نمی‌کنیم (افزایش دقت کلی سیستم)
        # اگر نیاز دارید حتی تارها هم شناسایی شوند، خط زیر را کامنت کنید
        # if not self.check_blur(cv2_img):
        #     print("⚠️ Image too blurry")
        #     return None
        
        faces = self.app.get(cv2_img)
        if len(faces) == 0: return None
        
        # buffalo_l دقیق‌ترین چهره را برمی‌گرداند، ما آن را می‌گیریم
        return faces[0].embedding


# ================= ابزارهای کمکی (Helpers) =================

def decode_image(base64_string):
    """
    تبدیل سریع Base64 به تصویر OpenCV بدون استفاده از PIL.
    این کار مصرف RAM و CPU را کاهش می‌دهد.
    """
    if "base64," in base64_string:
        base64_string = base64_string.split("base64,")[1]
    
    img_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


# ================= هندلر وب‌سوکت =================
async def handler(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            action = data.get("action")
            img_base64 = data.get("image")
            
            cv2_img = None
            if img_base64:
                cv2_img = decode_image(img_base64)
            
            # --- اکشن ثبت نام ---
            if action == "register":
                name = data.get("name", "").strip()
                if not name:
                    await websocket.send(json.dumps({"status": "error", "message": "نام الزامی است"}))
                    continue
                
                if cv2_img is None:
                    await websocket.send(json.dumps({"status": "error", "message": "تصویر نامعتبر"}))
                    continue
                
                # پردازش چهره
                embedding = face_engine.get_embedding_from_image(cv2_img)
                
                if embedding is None:
                    await websocket.send(json.dumps({"status": "error", "message": "چهره واضحی یافت نشد"}))
                else:
                    db_id = await db.save_user(name, embedding)
                    
                    if db_id:
                        faiss_engine.add_user(db_id, embedding)
                        await websocket.send(json.dumps({
                            "status": "success",
                            "message": f"کاربر {name} ثبت شد"
                        }))
                    else:
                        await websocket.send(json.dumps({"status": "error", "message": "خطای دیتابیس"}))
            
            # --- اکشن احراز هویت ---
            elif action == "recognize_image":
                if cv2_img is None:
                    await websocket.send(json.dumps({"status": "error", "message": "تصویر نامعتبر"}))
                    continue
                
                embedding = face_engine.get_embedding_from_image(cv2_img)
                
                if embedding is None:
                    await websocket.send(json.dumps({"status": "success", "name": "No Face", "distance": 1.0}))
                else:
                    db_id, similarity = faiss_engine.search(embedding)
                    
                    if db_id:
                        # دریافت نام از دیتابیس (غیرهمگام)
                        name = await db.get_name_by_id(db_id)
                        # فاصله برای نمایش کاربر
                        distance_metric = 1 - similarity
                        response = {
                            "status": "success",
                            "name": name,
                            "distance": float(distance_metric)
                        }
                    else:
                        response = {
                            "status": "success",
                            "name": "Unknown",
                            "distance": 1.0
                        }
                    
                    await websocket.send(json.dumps(response))
            
            else:
                await websocket.send(json.dumps({"status": "error", "message": "Action invalid"}))
        
        except Exception as e:
            print(f"Server Error: {e}")
            await websocket.send(json.dumps({"status": "error", "message": str(e)}))


# ================= راه‌اندازی =================
async def main():
    global db, faiss_engine, face_engine
    
    print("Starting Optimized Server...")
    
    # راه‌اندازی دیتابیس (Async)
    db = AsyncPostgresFaceDB()
    await db.init_pool()
    
    faiss_engine = FaissSearchEngine()
    face_engine = FaceEngine()
    
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    if os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
        ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        print(f"✅ Secure WebSocket (WSS) running on wss://0.0.0.0:8765")
    else:
        print("⚠️ Running without SSL.")
        ssl_context = None
    
    async with websockets.serve(handler, "0.0.0.0", 8765, ssl=ssl_context, ping_interval=20):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")