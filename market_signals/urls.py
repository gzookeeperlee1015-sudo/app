from django.urls import path
from . import views

urlpatterns = [
    path('api/dashboard/', views.get_market_dashboard_data, name='market_dashboard'),
]
