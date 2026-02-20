# constitution/constitutional_guardrails.py

class ConstitutionalAI:
    """
    Layer 6 & 8: Konstitusi Sistem dan Ethical Guardrails.
    Mengevaluasi setiap rekomendasi taktis/strategis AI terhadap prinsip absolut institusi.
    """
    def __init__(self):
        # Konstitusi Absolut Ujung Langit Foundation
        self.principles = {
            1: "Institutional Survival > Short-Term Profit",
            2: "Capital Integrity > Growth Speed",
            3: "Transparency > Tactical Opacity",
            4: "Sovereignty > Jurisdictional Convenience",
            5: "Legitimacy > Regulatory Arbitrage"
        }
        
        # Hard Constraint Thresholds
        self.min_cbss = 1.0  # Capital Buffer Stress Score tidak boleh < 1.0
        self.max_sei = 70.0  # Sovereignty Exposure Index tidak boleh > 70
        self.max_intel_alert = 3 # Intelligence Alert Level >= 4 otomatis memblokir ekspansi

    def evaluate_ai_recommendation(self, ai_proposal: str, expected_roi: float, 
                                   projected_cbss: float, projected_sei: float, 
                                   intel_alert_level: int):
        print(f"\n[?] CONSTITUTIONAL AI: Menilai Rekomendasi Algoritma Taktis...")
        print(f"    - Proposal AI   : '{ai_proposal}'")
        print(f"    - Proyeksi ROI  : {expected_roi}% (Sangat Menggiurkan)")
        
        # Evaluasi Kepatuhan Konstitusional (Transparency & Explainability Layer)
        violations = []
        
        if projected_cbss < self.min_cbss:
            violations.append(f"PELANGGARAN PRINSIP 1 & 2: Proyeksi CBSS turun ke {projected_cbss:.2f}. "
                              f"Risiko insolvensi mengancam Survival Institusi.")
            
        if projected_sei > self.max_sei:
            violations.append(f"PELANGGARAN PRINSIP 4: Proyeksi SEI naik ke {projected_sei:.2f}. "
                              f"Mengorbankan Kedaulatan demi kemudahan yurisdiksi.")
                              
        if intel_alert_level > self.max_intel_alert:
            violations.append(f"PELANGGARAN PRINSIP 1: Level Peringatan Rezim {intel_alert_level}. "
                              f"Ekspansi diabaikan karena risiko geopolitik sistemik yang membahayakan.")

        self._print_constitutional_verdict(ai_proposal, violations, expected_roi)
        
        if violations:
            return "REJECTED_BY_CONSTITUTION"
        return "APPROVED_FOR_BOARD_REVIEW"

    def _print_constitutional_verdict(self, proposal, violations, roi):
        print("="*75)
        print("   CONSTITUTIONAL SUPREME COURT - AI OVERSIGHT DASHBOARD")
        print("="*75)
        if not violations:
            print("[+] STATUS: KONSTITUSIONAL.")
            print(f"[+] Rekomendasi '{proposal}' selaras dengan nilai jangka panjang.")
            print("[+] Tindakan: Teruskan ke Board of Directors untuk legitimasi manusia.")
        else:
            print("[-] STATUS: INKONSTITUSIONAL (HARD BLOCK)!")
            print(f"[-] Algoritma taktis dibutakan oleh profit {roi}%. Constitutional Override AKTIF.")
            print("\n    [ALASAN PENOLAKAN - EXPLAINABILITY LAYER]:")
            for v in violations:
                print(f"    -> {v}")
            print("\n[-] Tindakan: Proposal dimusnahkan. Kembalikan AI ke Conservative Mode.")
        print("="*75)


if __name__ == "__main__":
    supreme_court = ConstitutionalAI()
    
    # Skenario: AI yang dilatih untuk mencari profit menemukan celah arbitrase regulasi di negara berisiko tinggi.
    # AI memproyeksikan ROI 45%, tetapi menghancurkan rasio ketahanan (CBSS turun) dan SEI meroket.
    
    supreme_court.evaluate_ai_recommendation(
        ai_proposal="Pindahkan 5 Miliar IDR Core Capital ke HIGH-RISK-NATION untuk Arbitrase Pajak & Obligasi.",
        expected_roi=45.0,
        projected_cbss=0.85, # Di bawah batas aman 1.0
        projected_sei=85.0,  # Sangat rentan (Sovereignty di atas 70)
        intel_alert_level=4  # Ada ancaman Regime Shift (Level 4)
    )