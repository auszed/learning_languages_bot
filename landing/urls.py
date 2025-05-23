from django.urls import path
from landing.views import index, pre_order
from django.views.generic import RedirectView

# import for the static files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='home', permanent=True)),  # Redirect root to home
    path('home', index, name="home"),
    path('preorder', pre_order, name="preorder"), 

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if we are in debug mode we enable the url
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
