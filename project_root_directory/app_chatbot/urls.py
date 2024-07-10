"""
URL mappings for the app_chatbot app.
"""
from django.urls import path

from app_chatbot import views

app_name = 'app_chatbot'

urlpatterns = [
    path('chatbot/', views.chatbot, name='chatbot'),
    path('ui-chatbot/', views.ui_chatbot, name='ui_chatbot'),
]
