from django.urls import path
from . import views

urlpatterns = [
    # 종목 목록 조회
    path('api/stocks/', views.stock_list, name='stock_list'),

    # 게임 시작 (랜덤 구간 데이터 반환)
    path('api/game/start/', views.game_start, name='game_start'),

    # 닉네임 로그인 또는 신규 플레이어 생성
    path('api/game/login/', views.login_or_create, name='login_or_create'),

    # 게임 결과 저장 및 자산 업데이트
    path('api/game/result/', views.save_result, name='save_result'),

    # 랭킹 조회
    path('api/game/ranking/', views.ranking, name='ranking'),
]
