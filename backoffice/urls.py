from django.contrib import admin
from django.urls import path
from django.views.decorators.http import require_POST
from backoffice.views import chat_view, profile_view, translation_user_message, response_ai_message, logout_view

app_name = 'portal'

urlpatterns = [
    path('chatbot/', chat_view, name='chatbot'),
    path('profile/', profile_view, name='profile'),
    path('post_translation_user_message/', translation_user_message, name='post_translation_user_message'),
    path('post_ai_response/', response_ai_message, name='post_ai_response'),
    path('logout/', require_POST(logout_view), name='logout'),
]
