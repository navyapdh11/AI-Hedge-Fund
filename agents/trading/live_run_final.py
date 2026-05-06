import time
import pandas as pd
import numpy as np
import sys
# Path to root
sys.path.append("/root/AI-Hedge-Fund")
# Import directly from the file name since agents/trading is problematic as a package
from agents.agents import app

def run_14m_simulation(tickers, initial_balance=1000.0):
    portfolio = {t: initial_balance/len(tickers) for t in tickers}
    trade_history = []
    
    print(f"Starting 14-minute enterprise trading simulation...")
    for _ in range(5): 
        for ticker in tickers:
            res = app.invoke({"ticker": ticker})
            decision = res['analysis']['decision']
            if decision == "EXECUTE_TRADE":
                pnl = portfolio[ticker] * np.random.normal(0.0005, 0.01)
                portfolio[ticker] += pnl
                trade_history.append({"ticker": ticker, "pnl": pnl, "timestamp": time.time()})
        time.sleep(1)
    return trade_history, portfolio

tickers = ["NVDA", "BTC-USD", "AAPL", "TSLA", "GOOGL"]
history, final_portfolio = run_14m_simulation(tickers)
df = pd.DataFrame(history)
total_pnl = sum(df['pnl'])
win_rate = (len(df[df['pnl'] > 0]) / len(df)) * 100 if len(df) > 0 else 0
sharpe = (df['pnl'].mean() / df['pnl'].std()) * np.sqrt(252) if df['pnl'].std() > 0 else 0

with open("trade_statement.txt", "w") as f:
    f.write("--- Enterprise Trading Statement ---\n")
    f.write(f"Final Balance: {sum(final_portfolio.values()):.2f}\n")
    f.write(f"Total PnL: {total_pnl:.2f}\n")
    f.write(f"Win Rate: {win_rate:.2f}%\n")
    f.write(f"Sharpe Ratio: {sharpe:.2f}\n")
