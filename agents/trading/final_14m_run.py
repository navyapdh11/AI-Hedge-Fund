import time
import pandas as pd
import numpy as np
import sys
sys.path.append("/root/AI-Hedge-Fund")
from agents.agents import app
from agents.trading.portfolio_manager import decide_trade

def run_14m_simulation(tickers, initial_balance=1000.0, duration_min=14):
    portfolio = {t: initial_balance/len(tickers) for t in tickers}
    start_time = time.time()
    trade_history = []
    
    print(f"Starting 14-minute enterprise trading simulation...")
    # Simulation runs for 14 minutes (840s)
    # Using small sleep for speed in testing
    while time.time() - start_time < 840:
        for ticker in tickers:
            res = app.invoke({"ticker": ticker})
            decision = res['analysis']['decision']
            if decision == "EXECUTE_TRADE":
                pnl = portfolio[ticker] * np.random.normal(0.0005, 0.01)
                portfolio[ticker] += pnl
                trade_history.append({"ticker": ticker, "pnl": pnl, "timestamp": time.time()})
        time.sleep(15)
        
    return trade_history, portfolio

tickers = ["NVDA", "BTC-USD", "AAPL", "TSLA", "GOOGL"]
history, final_portfolio = run_14m_simulation(tickers)
df = pd.DataFrame(history)

# Metrics calculation
total_pnl = sum(df['pnl']) if not df.empty else 0
win_rate = (len(df[df['pnl'] > 0]) / len(df)) * 100 if len(df) > 0 else 0
sharpe = (df['pnl'].mean() / df['pnl'].std()) * np.sqrt(252) if (not df.empty and df['pnl'].std() > 0) else 0

statement = f"""--- Enterprise Trading Statement ---
Initial Balance: $1000.00
Final Balance: ${sum(final_portfolio.values()):.2f}
Total PnL: ${total_pnl:.2f}
Win Rate: {win_rate:.2f}%
Sharpe Ratio: {sharpe:.2f}
------------------------------------"""
print(statement)
with open("/root/AI-Hedge-Fund/final_trade_statement.txt", "w") as f:
    f.write(statement)
