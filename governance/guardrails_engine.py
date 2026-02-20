# governance/guardrails_engine.py

class RiskAppetiteEnvelope:
    """
    RAE (Risk Appetite Envelope) mendefinisikan batas aman institusi.
    Setiap keputusan finansial harus berada di dalam envelope ini.
    """
    def __init__(self, profile_id="CONSERVATIVE_01"):
        self.profile_id = profile_id
        
        # Aturan Konstitusi Konservatif Ujung Langit Foundation:
        # 1. Tidak boleh ada transaksi keluar lebih dari 2 Miliar IDR sekaligus tanpa persetujuan khusus.
        self.max_single_outflow = 2000000000 
        
        # 2. Kategori risiko yang di-blacklist secara otomatis (Hard Constraint).
        self.restricted_risk_tags = ["HIGH_RISK_SPECULATION", "UNVERIFIED_JURISDICTION", "POLITICAL_DONATION"]

    def evaluate_proposal(self, proposed_amount: int, transaction_type: str, risk_tag: str):
        """
        Fungsi ini bertindak sebagai 'Pintu Gerbang'.
        Mengembalikan (True/False, Pesan_Alasan)
        """
        print(f"\n[?] GOVERNANCE ENGINE: Mengevaluasi Proposal Transaksi...")
        print(f"    - Tipe   : {transaction_type}")
        print(f"    - Nominal: {proposed_amount:,} IDR")
        print(f"    - Risiko : {risk_tag}")

        # Cek Hard Constraints (Batas Maksimal)
        if transaction_type == "OUTFLOW" and proposed_amount > self.max_single_outflow:
            return False, f"RAE BREACH: Nominal {proposed_amount:,} IDR melebihi batas aman transaksi tunggal ({self.max_single_outflow:,} IDR)."

        # Cek Risiko Terlarang
        if risk_tag in self.restricted_risk_tags:
            return False, f"RAE BREACH: Kategori risiko '{risk_tag}' diblokir oleh Konstitusi Institusi."

        return True, "APPROVED: Proposal berada di dalam Risk Appetite Envelope."


if __name__ == "__main__":
    # --- SIMULASI UJI COBA GOVERNANCE ---
    engine = RiskAppetiteEnvelope()

    print("="*60)
    print("SIMULASI: EKSEKUTIF MENGAJUKAN 3 PROPOSAL TRANSAKSI")
    print("="*60)

    # Proposal 1: Operasional Normal (Aman)
    status, msg = engine.evaluate_proposal(
        proposed_amount=500000000, 
        transaction_type="OUTFLOW", 
        risk_tag="STANDARD_OPERATIONAL"
    )
    print(f"[!] HASIL: {msg}")

    # Proposal 2: Eksekutif mencoba mentransfer 3 Miliar sekaligus (Melebihi Limit)
    status, msg = engine.evaluate_proposal(
        proposed_amount=3000000000, 
        transaction_type="OUTFLOW", 
        risk_tag="STRATEGIC_EXPANSION"
    )
    print(f"[!] HASIL: {msg}")

    # Proposal 3: Spekulasi Berbahaya (Crypto/Saham Gorengan)
    status, msg = engine.evaluate_proposal(
        proposed_amount=100000000, 
        transaction_type="OUTFLOW", 
        risk_tag="HIGH_RISK_SPECULATION"
    )
    print(f"[!] HASIL: {msg}")
    print("="*60)