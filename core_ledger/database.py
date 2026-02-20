# core_ledger/database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Perbaikan Path Import: Memanggil secara eksplisit dari root project
from core_ledger.models.financial_core import Base

# Strategi Infrastruktur: Gunakan SQLite untuk ThinkPad X280, 
# siapkan PostgreSQL untuk Sovereign Cloud Layer 0.
DATABASE_URL = os.getenv("SAFAR_DB_URL", "sqlite:///./safar_core_local.db")

# Argumen koneksi khusus SQLite (diabaikan jika menggunakan PostgreSQL)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Engine deterministik
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Session factory yang aman dan terisolasi
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Fungsi ini membaca seluruh metadata dari financial_core.py 
    dan membangun tabel-tabelnya ke dalam database.
    """
    print("[*] Menghubungkan ke Storage Engine...")
    Base.metadata.create_all(bind=engine)
    print(f"[*] Skema Financial Core berhasil diinisiasi secara deterministik pada: {DATABASE_URL}")

def get_db():
    """
    Generator untuk menyediakan sesi database yang aman.
    Akan otomatis ditutup setelah transaksi selesai untuk mencegah memory leak.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()