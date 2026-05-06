import time
import pandas as pd
import numpy as np
import sys
sys.path.append("/root/AI-Hedge-Fund/agents/trading")
from agents import app # Agents is in agents/trading/agents.py

def run_live_simulation(tickers, initial_balance=1000.0, duration_min=14):
    portfolio = {t: initial_balance/len(tickers) for t in tickers}
    start_time = time.time()
    trade_history = []
    
    print(f"Starting simulation...")
    for _ in range(5): 
        for ticker in tickers:
            res = app.invoke({"ticker": ticker})
            decision = res['analysis']['decision']
            if decision == "EXECUTE_TRADE":
                pnl = portfolio[ticker] * np.random.normal(0.001, 0.01)
                portfolio[ticker] += pnl
                trade_history.append({"ticker": ticker, "pnl": pnl, "timestamp": time.time()})
        time.sleep(2)
        
    return trade_history, portfolio

tickers = ["NVDA", "BTC-USD", "AAPL", "TSLA", "GOOGL"]
history, final_portfolio = run_live_simulation(tickers)
df = pd.DataFrame(history)
print(f"Portfolio: {final_portfolio}")
print(f"Total PnL: {sum(df['pnl'] if not df.empty else [0]):.2f}")
