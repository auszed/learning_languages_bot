from django.contrib import admin
from django.urls import path
from backoffice.views import chat_view

urlpatterns = [
    path('chatbot', chat_view, name='chatbot'),
]
