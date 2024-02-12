from django.urls import path
from .views import create_category, get_categories, create_stock, get_stock_dashboard, get_tags, create_tags

urlpatterns = [
    path('create_category/', create_category, name='create_category'),
    path('get_categories/', get_categories, name='get_categories'),
    path('create_stock/', create_stock, name='create_stock'),
    path('get_stock_dashboard/', get_stock_dashboard, name='stock_dashboard'),
    path('create_tags/', create_tags, name='create_tags'),
    path('get_tags/', get_tags, name='get_tags')
]