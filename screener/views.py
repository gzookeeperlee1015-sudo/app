"""
screener/views.py

4가지 카테고리 스크리너 API 뷰
  GET /api/stocks/growth/  → 저평가 성장주
  GET /api/stocks/value/   → 저렴한 가치주
  GET /api/stocks/week52/  → 52주 신고가 근접
  GET /api/stocks/volume/  → 거래량 상위 10
"""
import logging
from django.http import JsonResponse
from .cache import get_cached_data

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
        return JsonResponse(
            {"error": "데이터를 불러오는 중 문제가 발생했습니다.", "details": str(e)},
            status=500,
        )


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
