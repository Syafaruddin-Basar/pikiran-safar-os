# risk_engine/monte_carlo_engine.py

import numpy as np

class MonteCarloSimulator:
    """
    Engine Probabilistik Layer 2.
    Mensimulasikan ribuan skenario guncangan untuk menghitung Survival Probability 
    dan Capital Buffer Stress Score (CBSS).
    """
    def __init__(self, current_capital: float):
        self.current_capital = current_capital
        
    def run_capital_stress_test(self, iterations=10000, time_horizon_days=365):
        """
        Menjalankan simulasi Monte Carlo untuk menghitung potensi kerugian terburuk (Tail Risk).
        """
        # Asumsi Volatilitas Pasar Harian (Normal variance)
        daily_volatility = 0.002 # 0.2% volatilitas harian
        
        # Asumsi Probabilitas Macro Shock (Regime Shift, Liquidity Freeze)
        shock_probability = 0.01 # 1% kemungkinan terjadi shock per hari
        shock_impact_mean = -0.05 # Jika terjadi shock, rata-rata kerugian 5% dari modal
        shock_impact_std = 0.02   # Deviasi shock
        
        # Matriks Simulasi (Baris: Skenario, Kolom: Hari)
        np.random.seed(42) # Seed deterministik untuk replikasi hasil
        
        # 1. Simulasi Volatilitas Harian
        daily_returns = np.random.normal(0, daily_volatility, (iterations, time_horizon_days))
        
        # 2. Injeksi Skala Ekstrem
        shocks = np.random.binomial(1, shock_probability, (iterations, time_horizon_days))
        shock_magnitudes = np.random.normal(shock_impact_mean, shock_impact_std, (iterations, time_horizon_days))
        
        total_daily_returns = daily_returns + (shocks * shock_magnitudes)
        
        # 3. Hitung Kumulatif Pergerakan Modal
        cumulative_returns = np.prod(1 + total_daily_returns, axis=1)
        simulated_ending_capital = self.current_capital * cumulative_returns
        
        # 4. Kalkulasi Kerugian
        simulated_losses = self.current_capital - simulated_ending_capital
        
        # 5. Ekstraksi Tail Risk (95th Percentile Worst-Case Scenario)
        p95_loss = np.percentile(simulated_losses, 95)
        
        # 6. Hitung Capital Buffer Stress Score (CBSS)
        cbss = self.current_capital / p95_loss if p95_loss > 0 else float('inf')
        
        return cbss

if __name__ == "__main__":
    # Ini hanya dijalankan jika file ini dieksekusi langsung
    simulator = MonteCarloSimulator(current_capital=10000000000)
    cbss = simulator.run_capital_stress_test(iterations=10000, time_horizon_days=365)
    print(f"Test CBSS: {cbss}")