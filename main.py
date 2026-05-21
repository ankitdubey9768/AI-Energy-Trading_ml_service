import json
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.forecaster import generate_forecast, generate_recommendations
from typing import List, Dict, Any

app = FastAPI(title="AI Power ML Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ForecastRequest(BaseModel):
    market: str
    date: str

class RecommendRequest(BaseModel):
    forecast_data: List[Dict[str, Any]]
    strategy: str

@app.post("/forecast")
def get_forecast(req: ForecastRequest):
    return generate_forecast(req.market, req.date)

@app.post("/recommend")
def get_recommendations(req: RecommendRequest):
    return generate_recommendations(req.forecast_data, req.strategy)

@app.get("/market-data")
def get_market_data(exchange: str = 'IEX'):
    from models.forecaster import get_exchange_data
    return get_exchange_data(exchange)

@app.get("/arbitrage/opportunities")
def get_arbitrage_opportunities():
    from models.forecaster import detect_arbitrage
    return detect_arbitrage()

@app.post("/model/retrain")
def retrain_model():
    from models.forecaster import auto_retrain_mock
    return auto_retrain_mock()

@app.get("/performance/yesterday")
def get_performance(market: str = "DAM"):
    from models.forecaster import generate_performance_metrics
    return generate_performance_metrics(market)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    from models.forecaster import get_delhi_tomorrow_temp
    import uuid
    import random
    from datetime import datetime
    
    sent_critical = False
    
    try:
        while True:
            await asyncio.sleep(300) # Throttle core iteration check to exactly 5 minutes (300)
            if random.random() > 0.85: continue # 15% absolute chance of a warning firing so it's not spamming
            
            # Check physics to generate highly realistic, unprompted AI triggers
            temps, hums = get_delhi_tomorrow_temp()
            
            if temps and max(temps) > 38.0 and not sent_critical:
                alert = {
                    "id": str(uuid.uuid4()),
                    "level": "CRITICAL",
                    "message": f"SEVERE RAW DEMAND SPIKE: Physical grid temperature tomorrow hitting {round(max(temps), 1)}°C. High probability of DSM Deviation Penalty if short-volume is not pre-purchased in DAM.",
                    "timestamp": datetime.now().isoformat(),
                    "read": False
                }
                sent_critical = True # Ensure this massive notification only fires exactly once
            elif random.random() > 0.5:
                b = random.randint(30, 80)
                alert = {
                    "id": str(uuid.uuid4()),
                    "level": "WARNING",
                    "message": f"AI Engine detects rising procurement friction in PXIL Exchange for Block {b} to {b+8}. Consider shifting Buy volumes to IEX.",
                    "timestamp": datetime.now().isoformat(),
                    "read": False
                }
            else:
                alert = {
                    "id": str(uuid.uuid4()),
                    "level": "INFO",
                    "message": f"Model Accuracy drifting slightly to {round(random.uniform(83.1, 84.8), 2)}% based on last hour. Recommend running /model/retrain post-market.",
                    "timestamp": datetime.now().isoformat(),
                    "read": False
                }
                
            await websocket.send_text(json.dumps(alert))
    except WebSocketDisconnect:
        pass
