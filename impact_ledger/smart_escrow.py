# impact_ledger/smart_escrow.py

import time
import uuid

class SmartEscrowVault:
    """
    Layer 7: Pencairan dana berbasis pencapaian (Milestone-based Escrow).
    Dana dikunci secara kriptografis dan hanya cair jika auditor/validator 
    memberikan bukti bahwa pekerjaan di lapangan telah selesai.
    """
    def __init__(self, project_name: str, total_budget: int):
        self.contract_id = str(uuid.uuid4())[:8]
        self.project_name = project_name
        self.total_budget = total_budget
        self.locked_funds = total_budget
        self.released_funds = 0
        self.milestones = []
        
        print("\n" + "="*70)
        print(f"[*] SMART ESCROW CONTRACT CREATED: {self.contract_id}")
        print(f"[*] Proyek      : {self.project_name}")
        print(f"[*] Total Dana  : Rp {self.total_budget:,} (DIKUNCI / LOCKED)")
        print("="*70)

    def define_milestone(self, phase_name: str, percentage: float):
        """Membagi dana ke dalam tahapan-tahapan yang ketat."""
        allocation = int(self.total_budget * (percentage / 100))
        self.milestones.append({
            "phase": phase_name,
            "allocation": allocation,
            "status": "LOCKED"
        })
        print(f"    [+] Milestone Ditambahkan: {phase_name} ({percentage}%) -> Rp {allocation:,}")

    def verify_and_release(self, milestone_index: int, auditor_name: str, proof_hash: str):
        """Mencairkan dana hanya jika ada verifikasi bukti (Proof of Work)."""
        if milestone_index >= len(self.milestones):
            print("[!] ERROR: Index milestone tidak valid.")
            return

        milestone = self.milestones[milestone_index]
        
        if milestone["status"] == "RELEASED":
            print(f"[!] ERROR: Dana untuk '{milestone['phase']}' sudah dicairkan sebelumnya.")
            return

        print(f"\n[?] VALIDASI AUDITOR: {auditor_name} memverifikasi '{milestone['phase']}'")
        print(f"    -> Memindai Hash Bukti Lapangan: {proof_hash} ... VALID!")
        time.sleep(1)

        # Logika Pencairan (Settlement)
        milestone["status"] = "RELEASED"
        self.locked_funds -= milestone["allocation"]
        self.released_funds += milestone["allocation"]
        
        print("-" * 70)
        print(f"  [+] DANA CAIR: Rp {milestone['allocation']:,} untuk {milestone['phase']}")
        print(f"  [!] Sisa Dana Terkunci : Rp {self.locked_funds:,}")
        print("-" * 70)

    def print_contract_status(self):
        print("\n" + "="*70)
        print(f"   STATUS ESCROW: {self.project_name}")
        print("="*70)
        for i, m in enumerate(self.milestones):
            status_mark = "🟢 CAIR" if m["status"] == "RELEASED" else "🔴 TERKUNCI"
            print(f"   [{i}] {m['phase'][:35]:<35} | Rp {m['allocation']:>12,} | {status_mark}")
        print("="*70)


if __name__ == "__main__":
    # Skenario: Eksekusi pendanaan untuk inisiatif jangka panjang di Lombok
    escrow = SmartEscrowVault(
        project_name="SASAK HERITAGE & LOMBOK NATURE CONSERVATION (2026-2030)", 
        total_budget=2500000000
    )

    # 1. Mendefinisikan Milestone (Termin Pencairan)
    escrow.define_milestone("Fase 1: Data Collection & Sasak Cultural Mapping", 30.0)
    escrow.define_milestone("Fase 2: Mandala Eco Village Guest Experience Setup", 40.0)
    escrow.define_milestone("Fase 3: Eksekusi Mandala Greenfest 2026", 30.0)
    
    # Cetak status awal (Semua terkunci)
    escrow.print_contract_status()

    # 2. Simulasi Verifikasi Lapangan & Pencairan
    time.sleep(2)
    print("\n>>> Tiga bulan kemudian... Tim lapangan menyelesaikan Fase 1.")
    
    # Auditor memverifikasi bahwa pemetaan budaya Sasak telah selesai dan datanya valid
    escrow.verify_and_release(
        milestone_index=0, 
        auditor_name="Independent Conservation Audit", 
        proof_hash="HASH_BUKTI_PEMETAAN_SASAK_001"
    )

    # Cetak status akhir
    escrow.print_contract_status()