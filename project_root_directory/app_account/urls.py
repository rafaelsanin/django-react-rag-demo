"""
URL mappings for the app_account app.
"""
from django.urls import path

from app_account import views

app_name = 'app_account'

urlpatterns = [
    path('login/', views.view_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
]
