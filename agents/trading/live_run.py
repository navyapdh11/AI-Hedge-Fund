import time
import pandas as pd
from agents.trading.agents import app
from agents.trading.portfolio_manager import decide_trade

def run_live_simulation(tickers, initial_balance=100.0, duration_min=10):
    portfolio = {t: initial_balance/len(tickers) for t in tickers}
    start_time = time.time()
    trade_history = []
    
    print(f"Starting 10-minute trading simulation...")
    while time.time() - start_time < duration_min * 60:
        for ticker in tickers:
            res = app.invoke({"ticker": ticker})
            decision = res['analysis']['decision']
            if decision == "EXECUTE_TRADE":
                pnl = portfolio[ticker] * 0.01  # Mock return
                portfolio[ticker] += pnl
                trade_history.append({"ticker": ticker, "pnl": pnl, "status": "TRADE"})
        time.sleep(10) # 10s delay between cycles
        
    return trade_history, portfolio

tickers = ["NVDA", "BTC-USD", "AAPL", "TSLA", "GOOGL"]
history, final_portfolio = run_live_simulation(tickers)
df = pd.DataFrame(history)
print(df.describe())
print(final_portfolio)
