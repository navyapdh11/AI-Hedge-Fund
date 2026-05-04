import numpy as np

# G4H-RMA Technical Logic
def calculate_rma(data, period=14):
    return data.ewm(alpha=1/period, adjust=False).mean()

def get_technical_signal(ticker):
    # Simulated G4H-RMA signal logic
    prices = np.random.normal(100, 1, 100) # Mock data
    z_score = np.random.uniform(-3, 3)
    regime = "NORMAL"
    signal = "NEUTRAL"
    if z_score > 2.0: signal = "SHORT"
    elif z_score < -2.0: signal = "LONG"
    return {"signal": signal, "z_score": z_score, "regime": regime}

