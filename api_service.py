import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "agents"))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from agents import app
import time

service = FastAPI(title="AI-Hedge-Fund API")

@service.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response

service.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@service.get("/")
async def read_index():
    return FileResponse(os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html"))

@service.get("/analyze/{ticker}")
async def analyze_ticker(ticker: str):
    # Run the full orchestrator graph
    result = app.invoke({"ticker": ticker})
    return result

@service.get("/debug/{ticker}")
async def debug_ticker(ticker: str):
    # Return individual agent signals for deep inspection
    from agents.trading.technical import get_technical_signal
    return {
        "technical": get_technical_signal(ticker),
        "fundamental": "neutral",
        "sentiment": "positive",
        "news": "macro-stable"
    }
...
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(service, host="0.0.0.0", port=8000)
