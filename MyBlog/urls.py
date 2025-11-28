from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from chebitoch.sitemaps import PostSitemap, CategorySitemap, StaticViewSitemap
from django.conf import settings

sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}

# Normalize ADMIN_URL from settings (strip leading/trailing slashes)
_admin_route = getattr(settings, 'ADMIN_URL', 'admin')
_admin_route = _admin_route.strip('/')  # ensure no leading/trailing slashes


urlpatterns = [
    path(f'{_admin_route}/', admin.site.urls),
    path('', include('chebitoch.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name='robots'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

