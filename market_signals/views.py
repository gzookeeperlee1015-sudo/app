"""
market_signals/views.py
"""
import logging
from django.http import JsonResponse
from .services.cache import get_cached_data

logger = logging.getLogger(__name__)


def _make_response(request, category_key: str):
    try:
        data   = get_cached_data()
        stocks = data.get("screens", {}).get(category_key, [])
        for i, stock in enumerate(stocks, 1):
            stock["rank"] = i
        return JsonResponse({
            "category":   category_key,
            "count":      len(stocks),
            "total":      data.get("total", 0),
            "updated_at": data.get("updated_at", ""),
            "stocks":     stocks,
        }, json_dumps_params={"ensure_ascii": False})
    except Exception as e:
        logger.error(f"[{category_key}] 오류: {e}")
        return JsonResponse({"error": "데이터를 불러오는 중 문제가 발생했습니다.", "details": str(e)}, status=500)


def get_growth_stocks(request):
    """저평가 성장주 - GET /api/stocks/growth/"""
    return _make_response(request, "growth_undervalued")

def get_value_stocks(request):
    """저렴한 가치주 - GET /api/stocks/value/"""
    return _make_response(request, "value_stock")

def get_week52_high_stocks(request):
    """52주 신고가 근접 - GET /api/stocks/week52/"""
    return _make_response(request, "week52_high")

def get_volume_stocks(request):
    """거래량 상위 10 - GET /api/stocks/volume/"""
    return _make_response(request, "high_volume")

def get_market_dashboard_data(request):
    return JsonResponse({
        "market_signals": {
            "short_term": {"label": "중립", "status": "Y"},
            "long_term":  {"label": "매수", "status": "G"},
        },
        "indices": {
            "kospi":  {"name": "코스피", "price": "2500.00", "change_percent": "0.5%", "change_price": "12.5", "exposure_guide": "80-100%", "is_up": True},
            "kosdaq": {"name": "코스닥", "price": "750.00",  "change_percent": "0.3%", "change_price": "2.3",  "exposure_guide": "80-100%", "is_up": True},
        },
        "last_updated": "",
        "chart_data": [
            {"date": "03-01", "kospi": 2600, "ma20": 0.2, "ma200": 0.4,  "adr": 80},
            {"date": "03-08", "kospi": 2620, "ma20": 0.3, "ma200": 0.38, "adr": 95},
            {"date": "03-15", "kospi": 2680, "ma20": 0.6, "ma200": 0.45, "adr": 110},
            {"date": "03-22", "kospi": 2650, "ma20": 0.5, "ma200": 0.42, "adr": 100},
            {"date": "03-29", "kospi": 2750, "ma20": 0.8, "ma200": 0.5,  "adr": 120},
        ],
    }, json_dumps_params={"ensure_ascii": False})