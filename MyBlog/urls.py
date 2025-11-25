from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include


# Normalize ADMIN_URL from settings (strip leading/trailing slashes)
_admin_route = getattr(settings, 'ADMIN_URL', 'admin')
_admin_route = _admin_route.strip('/')  # ensure no leading/trailing slashes


urlpatterns = [
    path(f'{_admin_route}/', admin.site.urls),
    path('', include('chebitoch.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
