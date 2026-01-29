from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost, Post, Profile
from django.contrib.auth.models import User


class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'daily'

    def items(self):
        return ['home', 'about_us', 'blog_list', 'privacy_policy']

    def location(self, item):
        return reverse(item)


class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return BlogPost.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('blog_detail', args=[obj.slug])


class ProfileSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return User.objects.filter(is_active=True)[:1000]

    def lastmod(self, obj):
        return obj.profile.updated_at if hasattr(obj, 'profile') else None

    def location(self, obj):
        return reverse('profile', args=[obj.username])
