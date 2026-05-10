from django.urls import path
from . import views

# stock_game 앱의 URL 패턴
urlpatterns = [
    # 종목 목록 조회
    path('api/stocks/', views.stock_list, name='stock_list'),

    # 게임 시작 (랜덤 구간 데이터 반환)
    path('api/game/start/', views.game_start, name='game_start'),
]
