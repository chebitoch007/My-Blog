# chebitoch/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post, Category


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return reverse('category_posts', args=[obj.slug])


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return ['home', 'about']

    def location(self, item):
        return reverse(item)


# ===== UPDATE YOUR MAIN urls.py =====
# MyBlog/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from chebitoch.sitemaps import PostSitemap, CategorySitemap, StaticViewSitemap

sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chebitoch.urls')),

    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name='robots'),
]

# ===== CREATE robots.txt TEMPLATE =====
# Create this file: chebitoch/templates/robots.txt

"""
User-agent: *
Allow: /

Sitemap: {{ request.scheme }}://{{ request.get_host }}/sitemap.xml

# Block admin and sensitive areas
Disallow: /secure-panel-93b4c7f2/
Disallow: /media/private/

# Allow images and static files
Allow: /static/
Allow: /media/
"""