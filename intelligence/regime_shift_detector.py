# intelligence/regime_shift_detector.py

from datetime import datetime

class RegimeShiftDetector:
    """
    Layer 5: Mendeteksi perubahan arah sistemik dan pergeseran rezim (Regime Shift)
    melalui analisis narasi (Narrative Drift) dan kecepatan kebijakan (Policy Velocity).
    """
    def __init__(self):
        # Kamus bobot sentimen geopolitik dan regulasi (NLP Sederhana)
        self.risk_keywords = {
            "national security": 3,
            "capital control": 5,
            "sanction": 4,
            "emergency powers": 5,
            "data localization": 3,
            "retroactive": 4,
            "foreign interference": 2,
            "freeze": 4,
            "currency intervention": 3
        }

    def analyze_intelligence_feed(self, jurisdiction: str, news_feed: list):
        print(f"\n[~] STRATEGIC INTELLIGENCE ENGINE: Memindai Sinyal Geopolitik...")
        print(f"    - Target Yurisdiksi: {jurisdiction}")
        print(f"    - Waktu Pemindaian : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        total_risk_score = 0
        detected_signals = []

        # 1. Narrative Drift Analyzer & Policy Velocity Tracker
        for text in news_feed:
            text_lower = text.lower()
            for keyword, weight in self.risk_keywords.items():
                if keyword in text_lower:
                    total_risk_score += weight
                    detected_signals.append((keyword, weight, text))

        # 2. Klasifikasi Peringatan Dini (Early Warning Categories)
        alert_level, recommendation = self._classify_alert(total_risk_score)
        
        self._print_intelligence_dashboard(jurisdiction, detected_signals, total_risk_score, alert_level, recommendation)
        return alert_level

    def _classify_alert(self, score: int):
        # Kategori Alert berdasarkan Bagian VII APLIKASI PIKIRAN SAFAR
        if score >= 15:
            return "LEVEL 5 - Active Regime Disruption", "HARD BLOCK. Aktifkan Emergency Governance. Migrasi Data & Modal sekarang!"
        elif score >= 10:
            return "LEVEL 4 - Imminent Regime Shift", "Sovereignty Alert. Persiapkan evakuasi yurisdiksi dan tekan Risk Appetite Envelope."
        elif score >= 7:
            return "LEVEL 3 - Structural Realignment", "Peringatan Menengah. Tunda ekspansi modal ke wilayah ini."
        elif score >= 4:
            return "LEVEL 2 - Policy Acceleration", "Perubahan kebijakan terdeteksi cepat. Tingkatkan frekuensi monitoring."
        elif score >= 1:
            return "LEVEL 1 - Narrative Drift", "Pergeseran narasi terdeteksi. Belum ada aksi struktural yang dibutuhkan."
        else:
            return "LEVEL 0 - Stable Regime", "Lingkungan operasional stabil."

    def _print_intelligence_dashboard(self, jurisdiction, signals, score, alert, recommendation):
        print("="*70)
        print("   BOARD OF DIRECTORS - STRATEGIC INTELLIGENCE DASHBOARD")
        print("="*70)
        if not signals:
            print("[+] Tidak ada sinyal anomali terdeteksi. Lingkungan stabil.")
        else:
            print(f"[*] Total Sinyal Anomali Terdeteksi : {len(signals)}")
            print(f"[*] Akumulasi Policy Velocity Score : {score}")
            print("\n[-] Sinyal Kunci yang Terekam:")
            for keyword, weight, text in signals:
                print(f"    -> [Bobot: {weight}] Sinyal: '{keyword}' (Konteks: '{text}')")
        
        print("-" * 70)
        print(f"[*] STATUS REGIM : {alert}")
        print(f"[*] REKOMENDASI  : {recommendation}")
        print("="*70)


if __name__ == "__main__":
    engine = RegimeShiftDetector()
    
    # Simulasi 1: Umpan berita dari wilayah Netral
    feed_neutral = [
        "Pemerintah fokus pada perbaikan infrastruktur jalan raya.",
        "Kementerian teknologi meluncurkan program literasi digital baru."
    ]
    engine.analyze_intelligence_feed("ID-NEUTRAL-ZONE", feed_neutral)
    
    # Simulasi 2: Umpan berita dari wilayah yang sedang memanas secara geopolitik
    feed_hostile = [
        "Parlemen mendesak penggunaan emergency powers untuk mengatasi krisis energi.",
        "Bank Sentral diperkirakan akan menerapkan capital control minggu depan.",
        "Narasi perlindungan national security semakin menguat dalam pidato presiden.",
        "Regulator menuntut aturan data localization yang sangat ketat bagi entitas asing."
    ]
    engine.analyze_intelligence_feed("HIGH-RISK-NATION", feed_hostile)