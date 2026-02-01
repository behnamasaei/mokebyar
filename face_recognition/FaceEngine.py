import warnings

# مخفی کردن هشدارهای insightface برای تمیزی خروجی
warnings.filterwarnings("ignore")

import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import psycopg2
from psycopg2 import Error
import faiss
import os
import pickle

# ================= تنظیمات دیتابیس =================
DB_CONFIG = {
    "host": "localhost",
    "database": "mokebyar_db",
    "user": "postgres",
    "password": "root",
    "port": "5432"
}

INDEX_FILE = "faiss_index.bin"
ID_MAP_FILE = "id_map.pkl"


# ================= کلاس دیتابیس =================
class PostgresFaceDB:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        self.create_table()
    
    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            embedding BYTEA NOT NULL
        );
        '''
        self.cursor.execute(create_table_query)
        self.conn.commit()
        print("✅ Database table ready.")
    
    def get_all_users(self):
        self.cursor.execute("SELECT id, embedding FROM users")
        return self.cursor.fetchall()
    
    def save_user(self, name, embedding_bytes):
        """ذخیره کاربر و برگرداندن ID جدید (به روش استاندارد RETURNING)"""
        try:
            # RETURNING id بهترین روش است تا ID ساخته شده را بگیریم
            query = "INSERT INTO users (name, embedding) VALUES (%s, %s) RETURNING id"
            self.cursor.execute(query, (name, embedding_bytes))
            self.conn.commit()
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"❌ Error saving user: {e}")
            return None
    
    def get_name_by_id(self, user_id):
        self.cursor.execute("SELECT name FROM users WHERE id = %s", (user_id,))
        res = self.cursor.fetchone()
        return res[0] if res else None


# ================= موتور جستجوی Faiss =================
class FaissSearchEngine:
    def __init__(self, db):
        self.db = db
        self.dimension = 512
        self.index = None
        self.id_map = []
        self.load_or_build_index()
    
    def load_or_build_index(self):
        if os.path.exists(INDEX_FILE) and os.path.exists(ID_MAP_FILE):
            print("🚀 Loading existing Faiss index...")
            self.index = faiss.read_index(INDEX_FILE)
            with open(ID_MAP_FILE, 'rb') as f:
                self.id_map = pickle.load(f)
            print("✅ Index loaded.")
        else:
            print("🔄 Building Faiss index from Database (Please wait)...")
            self.build_index()
    
    def build_index(self):
        users = self.db.get_all_users()
        if not users:
            self.index = faiss.IndexFlatIP(self.dimension)
            self.id_map = []
            return
        
        vectors = []
        ids = []
        
        for user_id, blob in users:
            vec = np.frombuffer(blob, dtype=np.float32)
            vec = vec / np.linalg.norm(vec)  # نرمال‌سازی برای Cosine Similarity
            vectors.append(vec)
            ids.append(user_id)
        
        matrix = np.vstack(vectors).astype('float32')
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(matrix)
        self.id_map = ids
        
        faiss.write_index(self.index, INDEX_FILE)
        with open(ID_MAP_FILE, 'wb') as f:
            pickle.dump(self.id_map, f)
        print(f"✅ Index built for {len(ids)} users.")
    
    def add_user_to_index(self, db_id, embedding):
        vec = embedding / np.linalg.norm(embedding)
        self.index.add(np.array([vec]).astype('float32'))
        self.id_map.append(db_id)
        self.save_to_disk()
    
    def search(self, embedding, threshold=0.5):
        vec = embedding / np.linalg.norm(embedding)
        vec = np.array([vec]).astype('float32')
        
        k = 1
        distances, indices = self.index.search(vec, k)
        
        if indices[0][0] == -1:
            return None, None
        
        db_id = self.id_map[indices[0][0]]
        distance = 1 - distances[0][0]  # تبدیل Similarity به Distance
        
        if distance < threshold:
            name = self.db.get_name_by_id(db_id)
            return name, distance
        return None, distance
    
    def save_to_disk(self):
        faiss.write_index(self.index, INDEX_FILE)
        with open(ID_MAP_FILE, 'wb') as f:
            pickle.dump(self.id_map, f)


# ================= موتور چهره =================
class FaceEngine:
    def __init__(self):
        self.app = FaceAnalysis(name='buffalo_sc', providers=['CPUExecutionProvider'])
        self.app.prepare(ctx_id=-1, det_size=(640, 640))
    
    def get_embedding(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            print(f"❌ Image not found: {image_path}")
            return None
        faces = self.app.get(img)
        if len(faces) == 0:
            print(f"❌ No face detected in image.")
            return None
        return faces[0].embedding


# ================= برنامه اصلی =================
if __name__ == "__main__":
    db = PostgresFaceDB()
    search_engine = FaissSearchEngine(db)
    engine = FaceEngine()
    
    while True:
        print("\n" + "=" * 40)
        print("   FACE RECOGNITION (Faiss Accelerated)")
        print("=" * 40)
        print("1. Add New Person")
        print("2. Identify Person")
        print("3. Exit")
        
        choice = input("\nSelect: ").strip()  # حذف فاصله و نقطه اضافی
        
        if choice == '1':
            name = input("Name: ")
            path = input("Image Path: ")
            emb = engine.get_embedding(path)
            
            # اصلاح خطا: استفاده از is not None به جای if emb:
            if emb is not None:
                emb_bytes = emb.tobytes()
                # دریافت ID از SQL به روش صحیح
                new_id = db.save_user(name, emb_bytes)
                
                if new_id:
                    # ذخیره در Faiss
                    search_engine.add_user_to_index(new_id, emb)
                    print(f"✅ Saved with ID: {new_id}")
                else:
                    print("❌ Failed to save user to DB.")
        
        elif choice == '2':
            path = input("Image Path: ")
            emb = engine.get_embedding(path)
            
            # اصلاح خطا: استفاده از is not None
            if emb is not None:
                name, dist = search_engine.search(emb)
                if name:
                    print(f"✅ Identified: {name} (Dist: {dist:.4f})")
                else:
                    print("❌ Unknown person.")
        
        elif choice == '3':
            break
        
        else:
            print("Invalid option. Try again.")