from agents.trading.agents import app

if __name__ == "__main__":
    result = app.invoke({"ticker": "BTC-USD"})
    print("Orchestration complete:", result)
