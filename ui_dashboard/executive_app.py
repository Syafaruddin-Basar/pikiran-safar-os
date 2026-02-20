# ui_dashboard/executive_app.py

import streamlit as st
import sys
import os
from datetime import datetime, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import func
from core_ledger.database import SessionLocal
from core_ledger.models.financial_core import Entity, Account, AccountType, JournalLine
from risk_engine.monte_carlo_engine import MonteCarloSimulator
from sovereignty.sovereignty_engine import SovereigntyIndexCalculator
from intelligence.regime_shift_detector import RegimeShiftDetector
from impact_ledger.smart_escrow import SmartEscrowVault

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Pikiran Safar OS", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main {background-color: #0E1117;}
    h1, h2, h3 {color: #F0F2F6; font-family: 'Helvetica Neue', sans-serif; font-weight: 300;}
    .metric-card {
        background-color: #1E2127; border-radius: 10px; padding: 20px; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3); border: 1px solid #333;
    }
    .metric-card-danger {
        background-color: #3A1C1C; border-radius: 10px; padding: 20px; 
        box-shadow: 0 4px 6px rgba(255, 0, 0, 0.3); border: 1px solid #FF4B4B;
    }
    .status-aman {color: #00FF00; font-weight: bold;}
    .status-bahaya {color: #FF4B4B; font-weight: bold;}
    .escrow-box {
        background-color: #1A233A; border-left: 5px solid #00BFFF; padding: 15px; border-radius: 5px; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CHAOS CONTROL PANEL ---
st.sidebar.title("⚙️ Control Panel")
st.sidebar.markdown("Uji Ketahanan & Simulasi Proyek")
crisis_mode = st.sidebar.checkbox("🔥 Aktifkan Krisis Geopolitik", value=False)
simulate_project = st.sidebar.checkbox("✅ Verifikasi & Cairkan Fase 1 (Lombok)", value=False)

# --- FUNGSI PENGAMBILAN DATA (DYNAMIC BINDING) ---
@st.cache_data(ttl=10) # Cache singkat agar UI responsif
def fetch_system_data(is_crisis, is_phase1_done):
    db = SessionLocal()
    try:
        # 1. Financial Data 
        entity = db.query(Entity).filter(Entity.name == "Ujung Langit Foundation").first()
        if not entity:
            return None
        
        accounts = db.query(Account).filter(Account.entity_id == entity.entity_id, Account.account_type == AccountType.EQUITY).all()
        total_equity = 0
        for acc in accounts:
            credits = db.query(func.sum(JournalLine.credit_amount)).filter(JournalLine.account_id == acc.account_id).scalar() or 0
            debits = db.query(func.sum(JournalLine.debit_amount)).filter(JournalLine.account_id == acc.account_id).scalar() or 0
            total_equity += (credits - debits)

        # 2. Risk Data 
        simulator = MonteCarloSimulator(current_capital=total_equity)
        cbss_score = simulator.run_capital_stress_test(iterations=1000, time_horizon_days=365)

        # 3. Krisis Injeksi
        simulated_jurisdiction = "HIGH-RISK-NATION" if is_crisis else entity.jurisdiction_id
        capital_mobility = 10 if is_crisis else 90 
        
        feed = ["Parlemen mendesak penggunaan emergency powers."] if is_crisis else ["Stabilitas hukum kondusif."]

        # 4. Sovereignty & Intelligence
        sov_engine = SovereigntyIndexCalculator()
        sei_score = sov_engine.calculate_sei(entity.name, simulated_jurisdiction, capital_mobility)
        intel_engine = RegimeShiftDetector()
        alert_level = intel_engine.analyze_intelligence_feed(simulated_jurisdiction, feed)

        # 5. Smart Escrow Data (Layer 7)
        escrow = SmartEscrowVault("SASAK HERITAGE & LOMBOK NATURE CONSERVATION", 2500000000)
        escrow.define_milestone("Fase 1: Data Collection & Sasak Cultural Mapping", 30.0)
        escrow.define_milestone("Fase 2: Mandala Eco Village Guest Experience", 40.0)
        escrow.define_milestone("Fase 3: Eksekusi Mandala Greenfest 2026", 30.0)
        
        if is_phase1_done:
            escrow.verify_and_release(0, "Independent Audit", "HASH_VALID_001")

        return {
            "capital": total_equity, "cbss": cbss_score, "sei": sei_score, 
            "alert": alert_level, "jurisdiction": simulated_jurisdiction,
            "escrow_project": escrow.project_name,
            "escrow_locked": escrow.locked_funds,
            "escrow_released": escrow.released_funds,
            "escrow_milestones": escrow.milestones
        }
    finally:
        db.close()

# --- RENDER UI (FRONTEND) ---
def render_dashboard():
    st.title("Pikiran Safar OS")
    st.markdown("*Institutional Survival & Smart Escrow Dashboard*")
    
    if crisis_mode:
        st.error("⚠️ EMERGENCY GOVERNANCE MODE AKTIF: Guncangan Sistemik Terdeteksi!")
    
    data = fetch_system_data(crisis_mode, simulate_project)
    if not data:
        st.error("Sistem Belum Diinisiasi. Harap jalankan Genesis Block terlebih dahulu.")
        return

    # --- BARIS 1: METRIK UTAMA ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.subheader("Core Capital (Tier 1)")
        st.header(f"Rp {data['capital']:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        card_class = "metric-card" if data['cbss'] >= 1.0 else "metric-card-danger"
        st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
        st.subheader("Survival Probability")
        st.header(f"{data['cbss']:.2f}x Buffer")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        card_class = "metric-card" if data['sei'] < 70 else "metric-card-danger"
        st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
        st.subheader("Sovereignty Exposure")
        st.header(f"{data['sei']:.0f} / 100")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # --- BARIS 2: SMART ESCROW (LAYER 7) ---
    st.markdown("### 🔒 Smart Escrow: Execution Tracking")
    st.caption(f"**Proyek Aktif:** {data['escrow_project']}")
    
    ec1, ec2, ec3 = st.columns([1, 1, 2])
    with ec1:
        st.metric(label="Total Dana Terkunci (Locked)", value=f"Rp {data['escrow_locked']:,}")
    with ec2:
        st.metric(label="Dana Cair (Released)", value=f"Rp {data['escrow_released']:,}")
    with ec3:
        # Progress Bar
        progress_val = data['escrow_released'] / (data['escrow_locked'] + data['escrow_released'])
        st.progress(float(progress_val), text="Persentase Pencairan Dana")

    st.markdown("<br>", unsafe_allow_html=True)
    
    for i, m in enumerate(data['escrow_milestones']):
        status_icon = "🟢 **CAIR**" if m['status'] == "RELEASED" else "🔴 **TERKUNCI**"
        st.markdown(f"""
            <div class='escrow-box'>
                <strong>{m['phase']}</strong><br>
                Alokasi: Rp {m['allocation']:,} | Status: {status_icon}
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_dashboard()