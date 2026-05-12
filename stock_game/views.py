import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Player, GameResult
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
@require_GET
def stock_list(request):
    """종목 목록 반환 API"""
    return JsonResponse({"stocks": get_stock_list()})


@require_GET
def game_start(request):
    """
    게임 시작 API
    GET /api/game/start/?ticker=005930.KS
    랜덤 구간 주가 데이터 반환
    """
    ticker = request.GET.get("ticker")
    if not ticker:
        return JsonResponse({"error": "ticker가 필요합니다."}, status=400)

    data = get_random_game_data(ticker)
    if not data:
        return JsonResponse({"error": "데이터를 가져올 수 없습니다."}, status=500)

    return JsonResponse(data)


@csrf_exempt  # 외부 클라이언트(React)에서 POST 요청 허용
@require_POST
def login_or_create(request):
    """
    닉네임으로 로그인 또는 신규 플레이어 생성 API
    POST /api/game/login/
    body: { "nickname": "홍길동" }

    - 닉네임이 이미 존재하면 기존 플레이어 반환 (이전 자산 유지)
    - 없으면 새로 생성 (1000만원으로 시작)
    """
    body = json.loads(request.body)
    nickname = body.get("nickname", "").strip()

    if not nickname:
        return JsonResponse({"error": "닉네임을 입력해주세요."}, status=400)
    if len(nickname) > 20:
        return JsonResponse({"error": "닉네임은 20자 이하로 입력해주세요."}, status=400)

    # get_or_create: 닉네임이 있으면 가져오고, 없으면 새로 생성
    player, created = Player.objects.get_or_create(nickname=nickname)

    return JsonResponse({
        "nickname": player.nickname,
        "balance": player.balance,
        "is_new": created,  # True면 신규, False면 기존 플레이어
    })


@csrf_exempt
@require_POST
def save_result(request):
    """
    게임 결과 저장 API
    POST /api/game/result/
    body: {
        "nickname": "홍길동",
        "ticker": "005930.KS",
        "stock_name": "삼성전자",
        "start_balance": 10000000,
        "end_balance": 11500000
    }

    - 게임 결과를 DB에 저장
    - 플레이어의 누적 자산을 end_balance로 업데이트
    """
    body = json.loads(request.body)
    nickname = body.get("nickname")
    ticker = body.get("ticker")
    stock_name = body.get("stock_name")
    start_balance = body.get("start_balance")
    end_balance = body.get("end_balance")

    if not all([nickname, ticker, stock_name, start_balance, end_balance]):
        return JsonResponse({"error": "필수 값이 누락되었습니다."}, status=400)

    try:
        player = Player.objects.get(nickname=nickname)
    except Player.DoesNotExist:
        return JsonResponse({"error": "존재하지 않는 플레이어입니다."}, status=404)

    # 수익금과 수익률 계산
    profit = end_balance - start_balance
    profit_rate = ((end_balance - start_balance) / start_balance) * 100

    # 게임 결과 저장
    GameResult.objects.create(
        player=player,
        ticker=ticker,
        stock_name=stock_name,
        start_balance=start_balance,
        end_balance=end_balance,
        profit=profit,
        profit_rate=round(profit_rate, 2),
    )

    # 플레이어 누적 자산 업데이트
    player.balance = end_balance
    player.save()

    return JsonResponse({
        "message": "저장 완료",
        "nickname": player.nickname,
        "balance": player.balance,
        "profit": profit,
        "profit_rate": round(profit_rate, 2),
    })


@require_GET
def ranking(request):
    """
    랭킹 조회 API
    GET /api/game/ranking/

    - 전체 플레이어를 자산 기준 내림차순으로 정렬해 반환
    - 각 플레이어의 최근 게임 결과도 포함
    """
    players = Player.objects.order_by('-balance')[:20]  # 상위 20명

    ranking_data = []
    for i, player in enumerate(players):
        # 가장 최근 게임 결과 가져오기
        last_result = player.results.order_by('-played_at').first()

        ranking_data.append({
            "rank": i + 1,
            "nickname": player.nickname,
            "balance": player.balance,
            # 초기 자본 대비 전체 수익률
            "total_profit_rate": round(((player.balance - 10000000) / 10000000) * 100, 2),
            "last_stock": last_result.stock_name if last_result else None,
            "last_profit_rate": last_result.profit_rate if last_result else None,
        })

    return JsonResponse({"ranking": ranking_data})
