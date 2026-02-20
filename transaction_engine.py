# transaction_engine.py

import hashlib
from datetime import datetime, timezone
from core_ledger.database import SessionLocal
from core_ledger.models.financial_core import Entity, Account, AccountType, Ledger, TransactionEvent, JournalEntry, JournalLine

def inject_first_capital(amount: int):
    db = SessionLocal()
    try:
        print(f"=== MEMULAI TRANSAKSI INJEKSI MODAL: {amount} IDR ===")
        
        # 1. Tarik Data Entitas & Ledger Ujung Langit Foundation
        entity = db.query(Entity).filter(Entity.name == "Ujung Langit Foundation").first()
        if not entity:
            raise ValueError("Entitas Ujung Langit Foundation tidak ditemukan! Pastikan Genesis Block sudah dijalankan.")
        
        ledger = db.query(Ledger).filter(Ledger.entity_id == entity.entity_id, Ledger.locked_flag == False).first()
        if not ledger:
            raise ValueError("Tidak ada Ledger aktif untuk entitas ini.")

        # 2. Tarik Akun Core Capital (Equity) yang dibuat di Genesis Block
        equity_acc = db.query(Account).filter(Account.entity_id == entity.entity_id, Account.account_type == AccountType.EQUITY).first()
        
        # 3. Buat Akun Kas/Bank (Asset) karena ini transaksi pertama
        print("[*] Menyiapkan Chart of Accounts tujuan...")
        asset_acc = Account(
            entity_id=entity.entity_id,
            account_type=AccountType.ASSET,
            currency_id="IDR",
            risk_category="LIQUID_CASH",
            liquidity_class="HIGH"
        )
        db.add(asset_acc)
        db.flush() # Flush digunakan untuk mendapatkan ID tanpa melakukan commit permanen dulu
        
        print(f"    [+] Akun Tujuan (Asset/Kas) siap: {asset_acc.account_id}")
        print(f"    [+] Akun Sumber (Equity/Modal) siap: {equity_acc.account_id}")

        # 4. Ciptakan Transaction Event (Otorisasi & Keamanan)
        print("[*] Menghasilkan Kriptografi Transaksi...")
        event_payload = f"CAPITAL_INJECTION_{amount}_{datetime.now(timezone.utc).timestamp()}"
        event_hash = hashlib.sha256(event_payload.encode()).hexdigest()
        
        tx_event = TransactionEvent(
            event_type="CAPITAL_INJECTION",
            source_system="MANUAL_FOUNDER_INJECTION",
            authority_signature_hash="AUTH_FOUNDER_001", # Nantinya ini divalidasi oleh Governance Layer
            event_hash=event_hash
        )
        db.add(tx_event)
        db.flush()
        
        # 5. Ciptakan Journal Entry (Header Transaksi)
        print("[*] Mencatat Journal Entry...")
        journal = JournalEntry(
            ledger_id=ledger.ledger_id,
            event_id=tx_event.event_id,
            transaction_type="INITIAL_FUNDING",
            approval_status="APPROVED_BY_BOARD",
            total_debit=amount,
            total_credit=amount,
            created_by="SYSTEM_ADMIN"
        )
        db.add(journal)
        db.flush()
        
        # 6. Ciptakan Journal Lines (Detail Debit & Kredit)
        # Sisi Debit (Uang masuk ke entitas sebagai Kas/Bank)
        line_debit = JournalLine(
            journal_id=journal.journal_id,
            account_id=asset_acc.account_id,
            debit_amount=amount,
            credit_amount=0,
            currency_id="IDR",
            risk_tag="SAFE_LIQUIDITY"
        )
        
        # Sisi Kredit (Pencatatan asal dana, yaitu dari Modal Inti)
        line_credit = JournalLine(
            journal_id=journal.journal_id,
            account_id=equity_acc.account_id,
            debit_amount=0,
            credit_amount=amount,
            currency_id="IDR",
            risk_tag="CORE_EQUITY"
        )
        
        db.add(line_debit)
        db.add(line_credit)
        
        # VALIDASI MUTLAK LISKOV & CHAMBERS
        if journal.total_debit != journal.total_credit:
            raise ValueError("FATAL ERROR: Total Debit tidak sama dengan Total Credit!") [cite: 512]
            
        # Jika semua tahapan di atas lolos, baru kita simpan secara permanen
        db.commit()
        print(f"\n[+] TRANSAKSI BERHASIL DISAHKAN!")
        print(f"    Event Hash: {event_hash}")
        print(f"    Total Debit : {journal.total_debit} IDR")
        print(f"    Total Credit: {journal.total_credit} IDR")
        print("=== HUKUM DOUBLE-ENTRY BEKERJA SEMPURNA ===")
        
    except Exception as e:
        print(f"\n[!] TRANSAKSI DIBATALKAN (ROLLBACK): {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Suntikkan modal awal: 10.000.000.000 IDR (Gunakan Integer murni tanpa titik/koma)
    inject_first_capital(10000000000)