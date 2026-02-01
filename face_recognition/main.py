import asyncio
import pickle
import json
import numpy as np
import cv2
import insightface
from insightface.app import FaceAnalysis
import asyncpg
import faiss
import os
import base64
import warnings
import struct
from typing import Optional
# کتابخانه‌های FastAPI
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn

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
# در FastAPI معمولاً SSL در سطح سرور Uvicorn تنظیم می‌شود، نه در کد.
# اما مسافت‌ها برای استفاده‌های بعدی نگهداری می‌شوند.
CERT_FILE = '../MokebYar/localhost+2.pem'
KEY_FILE = '../MokebYar/localhost+2-key.pem'

INDEX_FILE = "faiss_index.bin"
ID_MAP_FILE = "id_map.pkl"
QUALITY_THRESHOLD = 100.0


# ================= مدل‌های Pydantic (برای Validation) =================
class RegisterRequest(BaseModel):
    name: str
    image: str  # Base64 string


class RecognizeRequest(BaseModel):
    image: str  # Base64 string


# ================= کلاس دیتابیس (نسخه Async) =================
class AsyncPostgresFaceDB:
    def __init__(self):
        self.pool = None
    
    async def init_pool(self):
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
        self.dimension = 512
        self.index = None
        self.id_map = []
        # بدون لاک کردن برای خوانایی ساده، اما برای ثبت‌نام همزمان باید مراقب بود.
        # در این نسخه فرض می‌کنیم ترافیک ثبت‌نام کم است یا ترتیب رعایت می‌شود.
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
            self.index = faiss.IndexFlatIP(self.dimension)
            self.id_map = []
    
    def add_user(self, db_id, embedding):
        vec = embedding / np.linalg.norm(embedding)
        self.index.add(np.array([vec]).astype('float32'))
        self.id_map.append(db_id)
        self.save_to_disk()
    
    def search(self, embedding, threshold=0.45):
        vec = embedding / np.linalg.norm(embedding)
        vec = np.array([vec]).astype('float32')
        
        k = 1
        distances, indices = self.index.search(vec, k)
        
        if indices[0][0] == -1: return None, None
        
        db_id = self.id_map[indices[0][0]]
        similarity = distances[0][0]
        
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
        self.app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
        self.app.prepare(ctx_id=-1, det_size=(640, 640))
        print("✅ buffalo_l model loaded.")
    
    def check_blur(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        score = cv2.Laplacian(gray, cv2.CV_64F).var()
        return score > QUALITY_THRESHOLD
    
    def get_embedding_from_image(self, cv2_img):
        if cv2_img is None: return None
        
        faces = self.app.get(cv2_img)
        if len(faces) == 0: return None
        
        return faces[0].embedding


# ================= ابزارهای کمکی =================
def decode_image(base64_string):
    if "base64," in base64_string:
        base64_string = base64_string.split("base64,")[1]
    
    img_data = base64.b64decode(base64_string)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


# ================= نمونه‌های سراسری =================
db: AsyncPostgresFaceDB = None
faiss_engine: FaissSearchEngine = None
face_engine: FaceEngine = None
loop = asyncio.get_event_loop()

# ================= راه‌اندازی FastAPI =================
app = FastAPI(title="MokebYar Face API")


@app.on_event("startup")
async def startup_event():
    global db, faiss_engine, face_engine
    print("Starting Optimized REST API Server...")
    
    # راه‌اندازی دیتابیس
    db = AsyncPostgresFaceDB()
    await db.init_pool()
    
    faiss_engine = FaissSearchEngine()
    face_engine = FaceEngine()


# ================= Endpoints =================

@app.post("/register")
async def register_user(request: RegisterRequest):
    """
    ثبت نام کاربر جدید با ارسال نام و تصویر Base64
    """
    try:
        name = request.name.strip()
        if not name:
            raise HTTPException(status_code=400, detail="نام الزامی است")
        
        # دیکد کردن تصویر
        cv2_img = decode_image(request.image)
        if cv2_img is None:
            raise HTTPException(status_code=400, detail="تصویر نامعتبر است")
        
        # پردازش چهره (CPU Bound) -> در Executor اجرا می‌شود تا Event Loop قفل نشود
        # این کار سرعت پاسخگویی سرور را در درخواست‌های همزمان حفظ می‌کند
        embedding = await loop.run_in_executor(None, face_engine.get_embedding_from_image, cv2_img)
        
        if embedding is None:
            raise HTTPException(status_code=400, detail="چهره واضحی یافت نشد")
        
        # ذخیره در دیتابیس
        db_id = await db.save_user(name, embedding)
        
        if db_id:
            # آپدیت Faiss (این بخش هم اگر خیلی شلوغ بود باید لاک می‌شد، اما فعلاً ساده نگه داشته می‌شود)
            await loop.run_in_executor(None, faiss_engine.add_user, db_id, embedding)
            return {"status": "success", "message": f"کاربر {name} ثبت شد", "user_id": db_id}
        else:
            raise HTTPException(status_code=500, detail="خطای دیتابیس")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Register Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recognize")
async def recognize_user(request: RecognizeRequest):
    """
    شناسایی چهره با ارسال تصویر Base64
    """
    try:
        cv2_img = decode_image(request.image)
        if cv2_img is None:
            raise HTTPException(status_code=400, detail="تصویر نامعتبر")
        
        # استخراج Embedding (CPU Bound)
        embedding = await loop.run_in_executor(None, face_engine.get_embedding_from_image, cv2_img)
        
        if embedding is None:
            return {"status": "success", "name": "No Face", "distance": 1.0}
        
        # جستجو در Faiss (CPU Bound)
        db_id, similarity = await loop.run_in_executor(None, faiss_engine.search, embedding)
        
        if db_id:
            name = await db.get_name_by_id(db_id)
            distance_metric = 1 - similarity
            return {
                "status": "success",
                "name": name,
                "distance": float(distance_metric)
            }
        else:
            return {
                "status": "success",
                "name": "Unknown",
                "distance": 1.0
            }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Recognize Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ================= اجرای برنامه =================
if __name__ == "__main__":
    # برای اجرا با SSL:
    # uvicorn main:app --host 0.0.0.0 --port 8765 --ssl-keyfile "../MokebYar/localhost+2-key.pem" --ssl-certfile "../MokebYar/localhost+2.pem"
    
    # برای اجرا بدون SSL (توسعه):
    uvicorn.run(app, host="0.0.0.0", port=8765)