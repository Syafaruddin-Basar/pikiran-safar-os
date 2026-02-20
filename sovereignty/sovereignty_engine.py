# sovereignty/sovereignty_engine.py

class SovereigntyIndexCalculator:
    """
    Sovereignty Exposure Index (SEI) mengukur kerentanan institusi 
    terhadap intervensi eksternal dari satu negara atau yurisdiksi.
    Skor 0-100. Semakin tinggi skor, semakin rentan institusi.
    """
    def __init__(self):
        # Database simulasi profil risiko yurisdiksi (Biasanya ditarik dari Layer 5 / Intelijen)
        self.jurisdiction_risk_database = {
            "ID-NEUTRAL-ZONE": {"political_risk": 10, "capital_control_risk": 5, "legal_dependency": 20},
            "US-MAINLAND": {"political_risk": 40, "capital_control_risk": 10, "legal_dependency": 80},
            "HIGH-RISK-NATION": {"political_risk": 90, "capital_control_risk": 85, "legal_dependency": 95}
        }

    def calculate_sei(self, entity_name: str, jurisdiction_id: str, capital_mobility_score: int):
        print(f"\n[~] SOVEREIGNTY ENGINE: Menganalisis Kedaulatan '{entity_name}'...")
        print(f"    - Yurisdiksi Terdaftar : {jurisdiction_id}")
        
        # Ambil profil negara
        country_profile = self.jurisdiction_risk_database.get(jurisdiction_id)
        if not country_profile:
            print("[!] Peringatan: Yurisdiksi tidak dikenal! Menggunakan default risiko maksimal.")
            country_profile = {"political_risk": 100, "capital_control_risk": 100, "legal_dependency": 100}

        # Formula Konseptual SEI (0 - 100)
        # SEI = f(Jurisdiction Diversification, Capital Mobility, Regulatory Risk)
        
        # Bobot Risiko (Berdasarkan parameter Bagian VI)
        weight_political = 0.4
        weight_capital_control = 0.4
        weight_legal = 0.2
        
        base_risk = (
            (country_profile["political_risk"] * weight_political) +
            (country_profile["capital_control_risk"] * weight_capital_control) +
            (country_profile["legal_dependency"] * weight_legal)
        )
        
        # Mobilitas modal mengurangi eksposur. Jika mobilitas tinggi (100), risiko turun.
        mobility_discount = (capital_mobility_score / 100.0) * 20 # Maksimal diskon 20 poin
        
        sei_score = max(0, min(100, base_risk - mobility_discount))
        
        self._print_sovereignty_dashboard(sei_score, jurisdiction_id)
        return sei_score

    def _print_sovereignty_dashboard(self, sei_score, jurisdiction_id):
        print("="*60)
        print("    BOARD OF DIRECTORS - SOVEREIGNTY EXPOSURE DASHBOARD")
        print("="*60)
        print(f"[*] Kategori Yurisdiksi       : {jurisdiction_id}")
        print(f"[*] Sovereignty Exposure Index: {sei_score:.2f} / 100")
        
        if sei_score > 70:
            print("[!] RED FLAG: Eksposur Kedaulatan Terlalu Tinggi!")
            print("[!] Tindakan : Segera siapkan Capital Freeze Migration dan Data Evacuation.")
        elif sei_score > 40:
            print("[-] WARNING: Risiko Menengah. Pertimbangkan diversifikasi multi-yurisdiksi.")
        else:
            print("[+] STATUS AMAN: Independensi operasional dan legal terjaga dengan baik.")
        print("="*60)


if __name__ == "__main__":
    engine = SovereigntyIndexCalculator()
    
    # Skenario 1: Ujung Langit Foundation di "ID-NEUTRAL-ZONE" dengan mobilitas modal tinggi
    engine.calculate_sei(
        entity_name="Ujung Langit Foundation (Core)", 
        jurisdiction_id="ID-NEUTRAL-ZONE", 
        capital_mobility_score=90
    )
    
    # Skenario 2: Entitas Operasional yang terjebak di negara berisiko tinggi
    engine.calculate_sei(
        entity_name="Subsidiary Alpha", 
        jurisdiction_id="HIGH-RISK-NATION", 
        capital_mobility_score=10 # Modal tertahan/sulit dipindah
    )