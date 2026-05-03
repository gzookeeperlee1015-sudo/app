from fastapi import FastAPI
from app.utils.data_fetcher import KisDataFetcher
from app.services.analyzer import MarketAnalyzer

app = FastAPI()

@app.get("/api/market-signal")
async def get_signal():
    fetcher = KisDataFetcher()
    token = fetcher.get_access_token()
    
    # 지수 데이터 수집 및 분석 실행[cite: 1]
    raw_data = fetcher.get_market_status(token)
    analyzer = MarketAnalyzer()
    analysis = analyzer.analyze(raw_data)
    
    return analysis