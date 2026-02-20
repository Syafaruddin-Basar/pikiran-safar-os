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

# --- 1. KONFIGURASI HALAMAN (MUST BE FIRST) ---
st.set_page_config(page_title="Pikiran Safar OS", layout="wide", initial_sidebar_state="expanded")

# --- 2. ADVANCED CSS INJECTION (PALANTIR / ENTERPRISE AESTHETIC) ---
st.markdown("""
    <style>
    /* Global Theme - Dark Military/Enterprise Terminal */
    .stApp { background-color: #050A15; color: #E2E8F0; font-family: 'Inter', -apple-system, sans-serif; }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Typography & Headers */
    h1, h2, h3, h4 { color: #F8FAFC; font-weight: 300; letter-spacing: -0.5px; }
    .os-title { font-size: 2.2rem; font-weight: 700; letter-spacing: 2px; color: #FFFFFF; text-transform: uppercase; margin-bottom: 0px;}
    .os-subtitle { font-size: 0.85rem; color: #64748B; font-family: monospace; letter-spacing: 1px; margin-bottom: 30px;}
    
    /* Section Headers (Layer 1, Layer 2, etc) */
    .layer-header { border-left: 3px solid #3B82F6; padding-left: 12px; margin-top: 40px; margin-bottom: 20px; font-size: 1.1rem; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px;}

    /* Executive Cards (Glassmorphism & Shadows) */
    .exec-card { background: #0F172A; border: 1px solid #1E293B; border-radius: 8px; padding: 24px; transition: all 0.3s ease; }
    .exec-card:hover { border-color: #3B82F6; box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1); }
    .exec-card-danger { background: #1C0A10; border: 1px solid #7F1D1D; border-radius: 8px; padding: 24px; box-shadow: inset 0 0 20px rgba(220, 38, 38, 0.05); }
    
    .card-title { font-size: 0.8rem; color: #64748B; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; font-weight: 600;}
    .card-value { font-size: 2.2rem; font-weight: 600; color: #F8FAFC; margin-bottom: 12px; font-family: 'Inter', sans-serif;}
    
    /* Status Badges */
    .badge-safe { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); color: #10B981; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-family: monospace; font-weight: 600;}
    .badge-warn { background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); color: #F59E0B; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-family: monospace; font-weight: 600;}
    .badge-danger { background: rgba(220, 38, 38, 0.1); border: 1px solid rgba(220, 38, 38, 0.3); color: #EF4444; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-family: monospace; font-weight: 600;}
    
    /* Smart Escrow Progress Bar Overlay */
    .escrow-item { background: #111827; border: 1px solid #1F2937; border-radius: 6px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;}
    .escrow-title { font-size: 0.9rem; font-weight: 500; color: #E2E8F0; }
    .escrow-amt { font-family: monospace; color: #94A3B8; font-size: 0.85rem;}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #0B0F19; border-right: 1px solid #1E293B; }
    </style>
""", unsafe_allow_html=True)

# --- 3. SIDEBAR: CHAOS CONTROL PANEL ---
st.sidebar.markdown("<div style='margin-bottom: 20px;'><span style='color:#3B82F6; font-family:monospace;'>[ SYS_ADMIN ]</span><br><b style='font-size:1.2rem; color:white;'>CONTROL TERMINAL</b></div>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border-color:#1E293B; margin-top:0px;'>", unsafe_allow_html=True)

crisis_mode = st.sidebar.toggle("⚠️ Inject Geopolitical Crisis", value=False, help="Simulasikan ancaman regulasi dan kapital dari negara operasional.")
simulate_project = st.sidebar.toggle("✅ Verify Milestone (Fase 1)", value=False, help="Simulasikan auditor independen memvalidasi pekerjaan lapangan.")

st.sidebar.markdown("<br><br><br><span style='color:#475569; font-size:0.7rem; font-family:monospace;'>PIKIRAN SAFAR OS v1.2<br>SECURE KERNEL ENCRYPTED</span>", unsafe_allow_html=True)

# --- 4. BACKEND DATA BINDING ---
@st.cache_data(ttl=5) 
def fetch_system_data(is_crisis, is_phase1_done):
    db = SessionLocal()
    try:
        entity = db.query(Entity).filter(Entity.name == "Ujung Langit Foundation").first()
        if not entity:
            return None
        
        accounts = db.query(Account).filter(Account.entity_id == entity.entity_id, Account.account_type == AccountType.EQUITY).all()
        total_equity = 0
        for acc in accounts:
            credits = db.query(func.sum(JournalLine.credit_amount)).filter(JournalLine.account_id == acc.account_id).scalar() or 0
            debits = db.query(func.sum(JournalLine.debit_amount)).filter(JournalLine.account_id == acc.account_id).scalar() or 0
            total_equity += (credits - debits)

        simulator = MonteCarloSimulator(current_capital=total_equity)
        cbss_score = simulator.run_capital_stress_test(iterations=1000, time_horizon_days=365)

        simulated_jurisdiction = "HIGH-RISK-NATION" if is_crisis else entity.jurisdiction_id
        capital_mobility = 10 if is_crisis else 90 
        feed = ["Pemerintah menerapkan emergency powers dan capital control."] if is_crisis else ["Stabilitas regulasi terjamin. Tidak ada anomali."]

        sov_engine = SovereigntyIndexCalculator()
        sei_score = sov_engine.calculate_sei(entity.name, simulated_jurisdiction, capital_mobility)
        intel_engine = RegimeShiftDetector()
        alert_level = intel_engine.analyze_intelligence_feed(simulated_jurisdiction, feed)

        escrow = SmartEscrowVault("SASAK HERITAGE & LOMBOK NATURE CONSERVATION", 2500000000)
        escrow.define_milestone("Fase 1: Data Collection & Cultural Mapping", 30.0)
        escrow.define_milestone("Fase 2: Mandala Eco Village Infrastructure", 40.0)
        escrow.define_milestone("Fase 3: Mandala Greenfest 2026", 30.0)
        
        if is_phase1_done:
            escrow.verify_and_release(0, "Independent Audit", "HASH_VALID_001")

        return {
            "capital": total_equity, "cbss": cbss_score, "sei": sei_score, 
            "alert": alert_level, "jurisdiction": simulated_jurisdiction,
            "escrow_project": escrow.project_name, "escrow_locked": escrow.locked_funds,
            "escrow_released": escrow.released_funds, "escrow_milestones": escrow.milestones
        }
    finally:
        db.close()

# --- 5. RENDER UI / FRONTEND ---
def render_dashboard():
    # Header HUD
    st.markdown(f"""
        <div class="os-title">PIKIRAN SAFAR OS</div>
        <div class="os-subtitle">INSTITUTIONAL OPERATING SYSTEM & ADAPTIVE GOVERNANCE [NODE: SECURE] // UTC: {datetime.now(timezone.utc).strftime('%H:%M:%S')}</div>
    """, unsafe_allow_html=True)
    
    if crisis_mode:
        st.error("🚨 **EMERGENCY GOVERNANCE MODE AKTIF:** Deteksi ancaman geopolitik sistemik. Konstitusi mengambil alih kontrol (Layer 8).")

    data = fetch_system_data(crisis_mode, simulate_project)
    if not data:
        st.warning("Sistem belum diinisiasi. Genesis Block tidak ditemukan.")
        return

    # --- SECTION A: FINANCIAL & SURVIVAL (LAYER 1 & 2) ---
    st.markdown("<div class='layer-header'>CORE SURVIVAL METRICS (LAYER 1 & 2)</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class='exec-card'>
                <div class='card-title'>Tier 1 Core Capital</div>
                <div class='card-value'>Rp {data['capital']:,.0f}</div>
                <span class='badge-safe'>LEDGER: IMMUTABLE</span>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        card_cls = "exec-card" if data['cbss'] >= 1.0 else "exec-card-danger"
        badge = "<span class='badge-safe'>STATUS: TAHAN KRISIS</span>" if data['cbss'] >= 1.0 else "<span class='badge-danger'>WARNING: TAIL RISK EXPOSURE</span>"
        st.markdown(f"""
            <div class='{card_cls}'>
                <div class='card-title'>Survival Probability (CBSS)</div>
                <div class='card-value'>{data['cbss']:.2f}x Buffer</div>
                {badge}
            </div>
        """, unsafe_allow_html=True)

    with col3:
        card_cls = "exec-card" if data['sei'] < 70 else "exec-card-danger"
        badge = f"<span class='badge-safe'>JURISDICTION: {data['jurisdiction']}</span>" if data['sei'] < 70 else f"<span class='badge-danger'>JURISDICTION: {data['jurisdiction']} (RED FLAG)</span>"
        st.markdown(f"""
            <div class='{card_cls}'>
                <div class='card-title'>Sovereignty Exposure (SEI)</div>
                <div class='card-value'>{data['sei']:.0f} <span style='font-size:1rem; color:#64748B;'>/ 100</span></div>
                {badge}
            </div>
        """, unsafe_allow_html=True)

    # --- SECTION B: INTELLIGENCE & CONSTITUTION (LAYER 5 & 6) ---
    st.markdown("<div class='layer-header'>INTELLIGENCE & CONSTITUTION (LAYER 5 & 6)</div>", unsafe_allow_html=True)
    
    ca, cb = st.columns(2)
    with ca:
        st.markdown(f"""
            <div class='exec-card' style='height: 100%;'>
                <div class='card-title'>Strategic Intelligence (NLP Pattern Detection)</div>
                <div style='font-family:monospace; margin-top:15px; margin-bottom:10px;'>{data['alert']}</div>
                <span style='color:#64748B; font-size:0.8rem;'>Memindai narasi kebijakan & risiko intervensi secara real-time.</span>
            </div>
        """, unsafe_allow_html=True)
        
    with cb:
        if data['cbss'] >= 1.0 and data['sei'] < 70 and "LEVEL 0" in data['alert']:
            const_status = "<span style='color:#10B981; font-weight:600;'>[ ✔ ] COMPLIANT:</span> Sistem beroperasi di dalam Risk Appetite Envelope."
            border = "border-color: #10B981;"
        else:
            const_status = "<span style='color:#EF4444; font-weight:600;'>[ ✘ ] HARD BLOCK AKTIF:</span> Pelanggaran kedaulatan terdeteksi. Ekspansi modal dibekukan."
            border = "border-color: #EF4444;"
            
        st.markdown(f"""
            <div class='exec-card' style='height: 100%; {border}'>
                <div class='card-title'>Constitutional AI Guardian</div>
                <div style='margin-top:15px; font-size:0.9rem;'>{const_status}</div>
            </div>
        """, unsafe_allow_html=True)

    # --- SECTION C: SMART ESCROW (LAYER 7) ---
    st.markdown("<div class='layer-header'>SMART ESCROW & IMPACT TRACKING (LAYER 7)</div>", unsafe_allow_html=True)
    
    st.markdown(f"<div style='color:#94A3B8; font-size:0.85rem; margin-bottom:15px; text-transform:uppercase;'>ACTIVE INITIATIVE: <b>{data['escrow_project']}</b></div>", unsafe_allow_html=True)
    
    ec1, ec2, ec3 = st.columns([1, 1, 2])
    with ec1:
        st.markdown(f"<div style='font-size:0.8rem; color:#64748B;'>LOCKED FUNDS</div><div style='font-size:1.5rem; font-weight:600; color:#F8FAFC;'>Rp {data['escrow_locked']:,}</div>", unsafe_allow_html=True)
    with ec2:
        st.markdown(f"<div style='font-size:0.8rem; color:#64748B;'>RELEASED FUNDS</div><div style='font-size:1.5rem; font-weight:600; color:#10B981;'>Rp {data['escrow_released']:,}</div>", unsafe_allow_html=True)
    with ec3:
        progress_val = data['escrow_released'] / (data['escrow_locked'] + data['escrow_released'])
        st.progress(float(progress_val))
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    for i, m in enumerate(data['escrow_milestones']):
        if m['status'] == "RELEASED":
            status_html = "<span class='badge-safe'>UNLOCKED & DEPLOYED</span>"
        else:
            status_html = "<span class='badge-danger' style='background:rgba(255,255,255,0.05); border-color:#334155; color:#64748B;'>LOCKED BY CONTRACT</span>"
            
        st.markdown(f"""
            <div class='escrow-item'>
                <div>
                    <div class='escrow-title'>[ Termin {i+1} ] {m['phase']}</div>
                    <div class='escrow-amt'>Allocation: Rp {m['allocation']:,}</div>
                </div>
                <div>{status_html}</div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_dashboard()
