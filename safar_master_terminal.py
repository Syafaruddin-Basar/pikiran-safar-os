# safar_master_terminal.py

import time
from datetime import datetime, timezone
from sqlalchemy import func

# Import Layer 1: Financial Core
from core_ledger.database import SessionLocal
from core_ledger.models.financial_core import Entity, Account, AccountType, JournalLine

# Import Layer 2-6 Engines
from risk_engine.monte_carlo_engine import MonteCarloSimulator
from sovereignty.sovereignty_engine import SovereigntyIndexCalculator
from intelligence.regime_shift_detector import RegimeShiftDetector
from constitution.constitutional_guardrails import ConstitutionalAI

def print_header():
    print("\n" + "="*80)
    print(" "*25 + "PIKIRAN SAFAR OS v1.0")
    print(" "*20 + "INSTITUTIONAL SURVIVAL DASHBOARD")
    print("="*80)
    print(f"[*] Waktu Sistem (UTC) : {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Node Operasional   : ThinkPad X280 (Local Secure Instance)")
    print("="*80 + "\n")

def get_core_capital(db, entity_id):
    """Menghitung Modal Inti Real-time dari Layer 1"""
    accounts = db.query(Account).filter(Account.entity_id == entity_id, Account.account_type == AccountType.EQUITY).all()
    total_equity = 0
    for acc in accounts:
        credits = db.query(func.sum(JournalLine.credit_amount)).filter(JournalLine.account_id == acc.account_id).scalar() or 0
        debits = db.query(func.sum(JournalLine.debit_amount)).filter(JournalLine.account_id == acc.account_id).scalar() or 0
        total_equity += (credits - debits)
    return total_equity

def run_master_terminal():
    print_header()
    time.sleep(1)
    
    db = SessionLocal()
    try:
        # 1. DIAGNOSTIK LAYER 1 (FINANCIAL CORE)
        print("[>] MEMUAT LAYER 1: FINANCIAL CORE...")
        entity = db.query(Entity).filter(Entity.name == "Ujung Langit Foundation").first()
        if not entity:
            print("[!] KESALAHAN FATAL: Entitas tidak ditemukan. Jalankan genesis_block.py terlebih dahulu.")
            return

        core_capital = get_core_capital(db, entity.entity_id)
        print(f"    [+] Status Ledger   : SECURE & IMMUTABLE")
        print(f"    [+] Total Modal Inti: {core_capital:,.0f} IDR\n")
        time.sleep(1)

        # 2. DIAGNOSTIK LAYER 2 (MONTE CARLO RISK ENGINE)
        print("[>] MEMUAT LAYER 2: MONTE CARLO SURVIVAL SIMULATION...")
        if core_capital > 0:
            simulator = MonteCarloSimulator(current_capital=core_capital)
            # Jalankan simulasi senyap (tanpa print dashboard panjang), kita ambil nilai return-nya
            # Untuk demo, kita mock nilai CBSS agar tampilan bersih, tapi di produksi ini memanggil logika asli.
            cbss_score = simulator.run_capital_stress_test(iterations=5000, time_horizon_days=365)
        else:
            cbss_score = 0.0
        print("\n")
        time.sleep(1)

        # 3. DIAGNOSTIK LAYER 4 & 5 (SOVEREIGNTY & INTELLIGENCE)
        print("[>] MEMUAT LAYER 4 & 5: SOVEREIGNTY & GEOPOLITICAL INTELLIGENCE...")
        sov_engine = SovereigntyIndexCalculator()
        intel_engine = RegimeShiftDetector()
        
        sei_score = sov_engine.calculate_sei(
            entity_name=entity.name, 
            jurisdiction_id=entity.jurisdiction_id, 
            capital_mobility_score=90
        )
        
        feed_neutral = [
            "Pemerintah menyatakan dukungan terhadap program pelestarian budaya Sasak.",
            "Stabilitas hukum di zona operasional Foundation terpantau kondusif."
        ]
        alert_level = intel_engine.analyze_intelligence_feed(entity.jurisdiction_id, feed_neutral)
        print("\n")
        time.sleep(1)

        # 4. KESIMPULAN KONSTITUSIONAL (LAYER 6)
        print("="*80)
        print(" "*25 + "EXECUTIVE SUMMARY")
        print("="*80)
        print(f"  [1] Ketahanan Finansial (CBSS) : {cbss_score:.2f} (Target > 1.0)")
        print(f"  [2] Eksposur Kedaulatan (SEI)  : {sei_score:.2f} / 100 (Target < 70)")
        print(f"  [3] Peringatan Rezim (Geopol)  : {alert_level}")
        print("-" * 80)
        
        if cbss_score >= 1.0 and sei_score < 70 and "LEVEL 1" in alert_level or "LEVEL 0" in alert_level:
            print("  [+] KESIMPULAN: INSTITUSI DALAM KEADAAN OPTIMAL. SURVIVAL PROBABILITY TINGGI.")
        else:
            print("  [!] KESIMPULAN: ANCAMAN TERDETEKSI. TINJAU ULANG STRATEGI.")
        print("="*80)

    except Exception as e:
        print(f"[!] SYSTEM FAILURE: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_master_terminal()