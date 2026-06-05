# ai/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/ai/analyze/', views.stock_analyze, name='stock_analyze'),
]
