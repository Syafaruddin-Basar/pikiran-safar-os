# balance_sheet.py

from sqlalchemy import func
from core_ledger.database import SessionLocal
from core_ledger.models.financial_core import Entity, Account, AccountType, JournalLine

def generate_balance_sheet():
    db = SessionLocal()
    try:
        print("\n" + "="*50)
        print(" "*10 + "UJUNG LANGIT FOUNDATION")
        print(" "*12 + "REAL-TIME BALANCE SHEET")
        print("="*50)
        
        # Tarik Entitas
        entity = db.query(Entity).filter(Entity.name == "Ujung Langit Foundation").first()
        if not entity:
            raise ValueError("Entitas tidak ditemukan.")

        # Ambil semua akun milik entitas ini
        accounts = db.query(Account).filter(Account.entity_id == entity.entity_id).all()
        
        total_assets = 0
        total_liabilities_equity = 0
        
        print(f"\n[ ASSETS / KEKAYAAN ]")
        for acc in accounts:
            if acc.account_type == AccountType.ASSET:
                # Untuk Aset: Saldo = Total Debit - Total Credit
                debits = db.query(func.sum(JournalLine.debit_amount)).filter(JournalLine.account_id == acc.account_id).scalar() or 0
                credits = db.query(func.sum(JournalLine.credit_amount)).filter(JournalLine.account_id == acc.account_id).scalar() or 0
                balance = debits - credits
                total_assets += balance
                print(f"  - Kas/Bank (Risk: {acc.risk_category}) : {balance:,} {acc.currency_id}")

        print(f"\n[ LIABILITIES & EQUITY / KEWAJIBAN & MODAL ]")
        for acc in accounts:
            if acc.account_type in [AccountType.EQUITY, AccountType.LIABILITY]:
                # Untuk Modal/Kewajiban: Saldo = Total Credit - Total Debit
                debits = db.query(func.sum(JournalLine.debit_amount)).filter(JournalLine.account_id == acc.account_id).scalar() or 0
                credits = db.query(func.sum(JournalLine.credit_amount)).filter(JournalLine.account_id == acc.account_id).scalar() or 0
                balance = credits - debits
                total_liabilities_equity += balance
                print(f"  - Modal Inti (Risk: {acc.risk_category}) : {balance:,} {acc.currency_id}")
        
        print("-" * 50)
        print(f"TOTAL ASSETS                 : {total_assets:,} IDR")
        print(f"TOTAL LIABILITIES & EQUITY   : {total_liabilities_equity:,} IDR")
        print("=" * 50)
        
        if total_assets != total_liabilities_equity:
            print("[!] WARNING: NERACA TIDAK SEIMBANG! INTEGRITAS LEDGER TERKOMPROMI.")
        else:
            print("[+] STATUS: NERACA SEIMBANG (BALANCED). INTEGRITAS TERJAMIN.")
            
    except Exception as e:
        print(f"[!] GAGAL MEMUAT NERACA: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    generate_balance_sheet()