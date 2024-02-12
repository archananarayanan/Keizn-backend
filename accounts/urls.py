from django.urls import path
from .views import register_user, user_login, user_logout, reset_password, get_users

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('reset/', reset_password, name='reset'),
    path('users/', get_users, name='reset'),
]