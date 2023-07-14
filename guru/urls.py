from django.urls import path
from .views import *

urlpatterns = [
    path('<str:stock>/', stock_records_view, name='stock_records'),
    path('', stock_stats_grid, name='stock_stats_grid'),
]
