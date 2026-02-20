# governance/multi_sig_vault.py

import hashlib
import time
import uuid

class MultiSigVault:
    """
    Sistem Otorisasi Multi-Signature (2-of-3).
    Mencegah Single Point of Failure (SPOF) pada level eksekutif.
    Tidak ada satu pun individu yang bisa mengeksekusi transaksi besar sendirian.
    """
    def __init__(self, required_signatures=2):
        self.required_signatures = required_signatures
        
        # 3 Dewan Direksi dengan "Private Key" masing-masing (Disimulasikan dengan Hash)
        self.board_members = {
            "Safar (Founder & CEO)": hashlib.sha256(b"Safar_Secure_Key_001").hexdigest(),
            "Jamie Dimon (CFO)": hashlib.sha256(b"Jamie_Secure_Key_002").hexdigest(),
            "John Elkington (Ethics)": hashlib.sha256(b"John_Secure_Key_003").hexdigest()
        }
        
        self.proposals = {}

    def create_proposal(self, title, amount, destination):
        proposal_id = str(uuid.uuid4())[:8]
        self.proposals[proposal_id] = {
            "title": title,
            "amount": amount,
            "destination": destination,
            "signatures": [],
            "status": "PENDING"
        }
        print(f"\n[+] PROPOSAL DIBUAT (ID: {proposal_id})")
        print(f"    Tujuan : {title} | Nominal: Rp {amount:,}")
        print(f"    Status : Menunggu {self.required_signatures} Tanda Tangan.")
        return proposal_id

    def sign_proposal(self, proposal_id, board_member_name, private_key_sim):
        if proposal_id not in self.proposals:
            print(f"[!] ERROR: Proposal {proposal_id} tidak ditemukan.")
            return

        proposal = self.proposals[proposal_id]
        
        if proposal["status"] == "EXECUTED":
            print(f"[!] ERROR: Proposal {proposal_id} sudah dieksekusi sebelumnya.")
            return

        # Verifikasi Kriptografi (Simulasi)
        expected_hash = self.board_members.get(board_member_name)
        provided_hash = hashlib.sha256(private_key_sim.encode()).hexdigest()

        if expected_hash != provided_hash:
            print(f"[!] AUTENTIKASI GAGAL untuk {board_member_name}! Kunci tidak valid.")
            return

        if board_member_name in proposal["signatures"]:
            print(f"[-] {board_member_name} sudah menandatangani proposal ini.")
            return

        proposal["signatures"].append(board_member_name)
        print(f"    [~] TANDA TANGAN DITERIMA: {board_member_name}")

        self._check_execution(proposal_id)

    def _check_execution(self, proposal_id):
        proposal = self.proposals[proposal_id]
        current_sigs = len(proposal["signatures"])
        
        print(f"    [*] Progress: {current_sigs}/{self.required_signatures} Signatures")
        
        if current_sigs >= self.required_signatures:
            proposal["status"] = "EXECUTED"
            print("="*65)
            print(f"  [!] KONSENSUS TERCAPAI (MULTI-SIG VALID)!")
            print(f"  [!] MENGIRIM DANA RP {proposal['amount']:,} KE {proposal['destination']}...")
            print("="*65)


if __name__ == "__main__":
    vault = MultiSigVault(required_signatures=2)
    
    print("\n" + "="*65)
    print("   SIMULASI TATA KELOLA MULTI-SIGNATURE (2-of-3 KEYHOLDERS)")
    print("="*65)

    # Skenario: Safar ingin mencairkan dana untuk proyek Lombok Nature Conservation
    proposal_id = vault.create_proposal(
        title="Pendanaan Sasak Heritage & Mandala Eco Village", 
        amount=2500000000, 
        destination="Rekening Operasional Lombok"
    )

    time.sleep(1)
    print("\n--- Safar mencoba mengeksekusi sendirian ---")
    vault.sign_proposal(proposal_id, "Safar (Founder & CEO)", "Safar_Secure_Key_001")
    
    # Perhatikan bahwa meskipun Safar adalah Founder, uang tidak akan bergerak karena baru 1 tanda tangan.
    time.sleep(1)
    print("\n--- Jamie Dimon (CFO) memvalidasi kelayakan finansial dan menyetujui ---")
    vault.sign_proposal(proposal_id, "Jamie Dimon (CFO)", "Jamie_Secure_Key_002")