from django.contrib import admin
from django.urls import path
from backoffice.views import chat_view, profile_view, translation_user_message, response_ai_message, logout_view

urlpatterns = [
    path('chatbot', chat_view, name='chatbot'),
    path('profile', profile_view, name='profile'),
    path('post_TranslationUserMessage', translation_user_message, name='post_TranslationUserMessage'),
    path('post_ai_response', response_ai_message, name='post_ai_response'),
    path('logout', logout_view, name='logout'),
]
