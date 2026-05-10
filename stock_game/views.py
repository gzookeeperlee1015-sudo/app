from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .services import get_stock_list, get_random_game_data


@require_GET
def stock_list(request):
    """
    게임 시작 화면에서 종목 선택 목록을 제공하는 API
    GET /api/stocks/

    Returns:
        {"stocks": [{"name": "삼성전자", "ticker": "005930.KS"}, ...]}
    """
    return JsonResponse({"stocks": get_stock_list()})


@require_GET
def game_start(request):
    """
    게임 시작 API - 선택한 종목의 랜덤 구간 데이터를 반환합니다.
    GET /api/game/start/?ticker=005930.KS

    Query Params:
        ticker: yfinance 티커 (필수)

    Returns:
        {
            "ticker": "005930.KS",
            "pivot_date": "2022-07-15",
            "history": [...],  # 과거 60일 (차트 표시용)
            "future": [...],   # 미래 30일 (게임 진행용, 프론트에서 하루씩 오픈)
        }
    """
    ticker = request.GET.get("ticker")

    # ticker가 없으면 400 Bad Request 반환
    if not ticker:
        return JsonResponse({"error": "ticker가 필요합니다."}, status=400)

    data = get_random_game_data(ticker)

    # 데이터를 가져오지 못하면 500 반환
    if not data:
        return JsonResponse({"error": "데이터를 가져올 수 없습니다."}, status=500)

    return JsonResponse(data)
