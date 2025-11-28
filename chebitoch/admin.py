from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_at', 'views_count']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content', 'keywords']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'author', 'category', 'status', 'featured_image')
        }),
        ('Article Body', {
            'fields': ('excerpt', 'content')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'keywords'),
            'classes': ('collapse',),
            'description': 'Leave blank to auto-generate from content'
        }),
        ('Statistics', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        })
    )

    readonly_fields = ['views_count']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'description')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        })
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'created_at', 'active']
    list_filter = ['active', 'created_at']
    search_fields = ['name', 'email', 'content']
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

    approve_comments.short_description = "Approve selected comments"