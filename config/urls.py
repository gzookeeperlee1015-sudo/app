# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('market_signals.urls')),   # 대시보드
    path('', include('stock_game.urls')),        # 주식 게임
    path('', include('screener.urls')),          # 종목 스크리너
    path('', include('ai_insight.urls')),                # AI 분석
]
