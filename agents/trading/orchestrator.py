import sys
import os
# Add the root directory to path
sys.path.insert(0, '/root/AI-Hedge-Fund')

from agents.trading.agents import app

if __name__ == "__main__":
    result = app.invoke({"ticker": "BTC-USD"})
    print("Orchestration complete:", result)
