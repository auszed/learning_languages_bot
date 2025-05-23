from django.urls import path
from .views import SignUpView, login_view, RootRedirectView

app_name = 'registration'

urlpatterns = [
    path('', RootRedirectView.as_view(), name='root'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', login_view, name='login'),
]