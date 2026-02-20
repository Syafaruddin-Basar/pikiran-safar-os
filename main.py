# main.py

from core_ledger.database import init_db

if __name__ == "__main__":
    print("=== APLIKASI PIKIRAN SAFAR: INITIALIZATION ===")
    print("Booting Layer 1: Financial Core...")
    
    # Membangun skema database
    init_db()
    
    print("=== LAYER 1 ONLINE ===")