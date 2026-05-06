import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))
from agents import app

if __name__ == "__main__":
    result = app.invoke({"ticker": "BTC-USD"})
    print("Orchestration complete:", result)
