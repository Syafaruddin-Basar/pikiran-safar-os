# genesis_block.py

import hashlib
from datetime import datetime, timezone
from core_ledger.database import SessionLocal
from core_ledger.models.financial_core import Entity, Account, AccountType, Ledger

def inject_genesis_block():
    db = SessionLocal()
    try:
        print("=== INISIASI GENESIS BLOCK ===")
        
        # 1. Buat Entitas Utama
        print("[*] Menciptakan Entitas Institusional...")
        ujung_langit_entity = Entity(
            name="Ujung Langit Foundation",
            jurisdiction_id="ID-NEUTRAL-ZONE", 
            risk_appetite_profile_id="CONSERVATIVE_01",
            capital_buffer_id="BUFFER_CORE_01"
        )
        db.add(ujung_langit_entity)
        db.commit()
        db.refresh(ujung_langit_entity)
        print(f"[+] Entitas Tercipta: {ujung_langit_entity.name}")
        print(f"    ID: {ujung_langit_entity.entity_id}")

        # 2. Buat Akun Dasar (Chart of Accounts)
        print("[*] Menginisiasi Struktur Chart of Accounts...")
        core_capital_acc = Account(
            entity_id=ujung_langit_entity.entity_id,
            account_type=AccountType.EQUITY,
            currency_id="IDR",
            risk_category="TIER_1_CAPITAL",
            liquidity_class="HIGH"
        )
        db.add(core_capital_acc)
        db.commit()
        db.refresh(core_capital_acc)
        print(f"[+] Akun Core Capital berhasil dibuat. (ID: {core_capital_acc.account_id})")

        # 3. Buat Ledger Genesis dengan Kriptografi
        print("[*] Mengunci Genesis Ledger...")
        # Menciptakan Immutable Hash untuk saldo awal (Zero State) yang baru
        genesis_hash = hashlib.sha256(b"UJUNG_LANGIT_FOUNDATION_GENESIS_ZERO_STATE").hexdigest()
        
        genesis_ledger = Ledger(
            entity_id=ujung_langit_entity.entity_id,
            opening_balance_hash=genesis_hash,
            period_start=datetime.now(timezone.utc),
            period_end=datetime.now(timezone.utc), # Akan di-update ke depan
            locked_flag=False
        )
        db.add(genesis_ledger)
        db.commit()
        print(f"[+] Genesis Ledger Terkunci!")
        print(f"    SHA-256 Hash: {genesis_hash}")
        
        print("\n=== GENESIS BLOCK BERHASIL DISUNTIKKAN ===")
        
    except Exception as e:
        print(f"[!] ERROR TERDETEKSI: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    inject_genesis_block()