"""
market_signals/views.py

4가지 카테고리 API 응답 처리
각 URL 요청 → 캐시에서 데이터 꺼내서 JSON 반환
"""

import logging
from django.http import JsonResponse
from .services.cache import get_cached_data

logger = logging.getLogger(__name__)


# ── 공통 헬퍼 ─────────────────────────────────
def _make_response(request, category_key: str):
    """
    캐시에서 특정 카테고리 데이터를 꺼내 JSON으로 반환
    4개 카테고리 뷰가 모두 이 함수를 사용합니다
    """
    try:
        data   = get_cached_data()
        stocks = data.get("screens", {}).get(category_key, [])

        # 순위 번호 추가
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
        return JsonResponse({
            "error":   "데이터를 불러오는 중 문제가 발생했습니다.",
            "details": str(e),
        }, status=500)


# ── 4가지 카테고리 뷰 ─────────────────────────
def get_growth_stocks(request):
    """저평가 성장주 - GET /api/stocks/growth/"""
    return _make_response(request, "growth_undervalued")


def get_value_stocks(request):
    """저렴한 가치주 - GET /api/stocks/value/"""
    return _make_response(request, "value_stock")


def get_dividend_stocks(request):
    """꾸준한 배당주 - GET /api/stocks/dividend/"""
    return _make_response(request, "dividend_stock")


def get_volume_stocks(request):
    """거래량 상위 10 - GET /api/stocks/volume/"""
    return _make_response(request, "high_volume")