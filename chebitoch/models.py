# models.py
import math
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO meta description (160 chars max)")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.meta_description and self.description:
            self.meta_description = self.description[:157] + '...' if len(self.description) > 160 else self.description
        super().save(*args, **kwargs)


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    featured_image = models.URLField(blank=True, null=True)

    # SEO Fields
    meta_title = models.CharField(max_length=70, blank=True, help_text="SEO title (60-70 chars)")
    meta_description = models.CharField(max_length=160, blank=True, help_text="SEO description (150-160 chars)")
    keywords = models.CharField(max_length=255, blank=True, help_text="Comma-separated keywords")

    # Performance
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at', 'status']),
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'category']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        # Auto-generate SEO fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:67] + '...' if len(self.title) > 70 else self.title

        if not self.meta_description:
            if self.excerpt:
                desc = self.excerpt
            else:
                desc = strip_tags(self.content)
            self.meta_description = desc[:157] + '...' if len(desc) > 160 else desc

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def get_read_time(self):
        """Calculates read time assuming 200 words per minute."""
        word_count = len(strip_tags(self.content).split())
        read_time = math.ceil(word_count / 200)
        return read_time if read_time > 0 else 1

    def increment_views(self):
        """Increment view count for analytics"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['post', 'active']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'