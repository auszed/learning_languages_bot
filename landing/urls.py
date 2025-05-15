from django.urls import path
from landing.views import index, pre_order, signin, sign_up_new

# import for the static files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home', index, name="home"),
    path('preorder', pre_order, name="preorder"), 
    path('signin', signin, name="signin"), 
    path('sign_up_new', sign_up_new, name="sign_up_new"), 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if we are in debug mode we enable the url
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

