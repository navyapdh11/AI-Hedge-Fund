import sys
sys.path.append("/root/AI-Hedge-Fund/agents/trading")
from agents import app

if __name__ == "__main__":
    result = app.invoke({"ticker": "BTC-USD"})
    print("Orchestration complete:", result)
