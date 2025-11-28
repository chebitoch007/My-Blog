from django.db.models import Q, Prefetch
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.cache import cache
from .models import Post, Category, Comment


def get_categories_cached():
    """Cache categories for 1 hour since they don't change often"""
    categories = cache.get('all_categories')
    if categories is None:
        categories = list(Category.objects.all())
        cache.set('all_categories', categories, 3600)  # 1 hour
    return categories


def search(request):
    query = request.GET.get('q', '').strip()
    results = []
    categories = get_categories_cached()

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(keywords__icontains=query),
            status='published'
        ).select_related('author', 'category').distinct()

    return render(request, 'chebitoch/search.html', {
        'query': query,
        'results': results,
        'categories': categories
    })


def home(request):
    # Optimize query with select_related to avoid N+1 queries
    posts = Post.objects.filter(status='published').select_related('author', 'category').only(
        'title', 'slug', 'excerpt', 'content', 'featured_image',
        'created_at', 'category__name', 'category__slug', 'author__username'
    )
    categories = get_categories_cached()

    # Pagination
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'chebitoch/home.html', context)


def post_detail(request, slug):
    # Optimize with select_related and prefetch_related
    post = get_object_or_404(
        Post.objects.select_related('author', 'category')
        .prefetch_related(
            Prefetch('comments', queryset=Comment.objects.filter(active=True))
        ),
        slug=slug,
        status='published'
    )

    # Increment views (async in production would be better)
    post.increment_views()

    comments = post.comments.all()  # Already prefetched
    categories = get_categories_cached()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        content = request.POST.get('content', '').strip()

        if name and email and content:
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                content=content
            )
            messages.success(request, 'Your comment has been added and is awaiting approval!')
            return redirect('post_detail', slug=slug)
        else:
            messages.error(request, 'Please fill in all fields.')

    context = {
        'post': post,
        'comments': comments,
        'categories': categories,
    }
    return render(request, 'chebitoch/post_detail.html', context)


def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)

    # Optimize query
    posts = Post.objects.filter(
        category=category,
        status='published'
    ).select_related('author', 'category').only(
        'category','title', 'slug', 'excerpt', 'content', 'featured_image',
        'created_at', 'author__username'
    )

    categories = get_categories_cached()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
    }
    return render(request, 'chebitoch/category_posts.html', context)


def about(request):
    categories = get_categories_cached()
    return render(request, 'chebitoch/about.html', {'categories': categories})