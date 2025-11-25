from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post, Category, Comment

def search(request):
    query = request.GET.get('q')
    results = []
    categories = Category.objects.all()  # Required for Navbar

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            status='published'
        ).distinct()

    return render(request, 'chebitoch/search.html', {
        'query': query,
        'results': results,
        'categories': categories
    })

def home(request):
    posts = Post.objects.filter(status='published')
    categories = Category.objects.all()

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
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    categories = Category.objects.all() # Added for navbar consistency

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')

        if name and email and content:
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                content=content
            )
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', slug=slug)

    context = {
        'post': post,
        'comments': comments,
        'categories': categories,
    }
    return render(request, 'chebitoch/post_detail.html', context)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    categories = Category.objects.all()

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
    categories = Category.objects.all() # Added for navbar consistency
    return render(request, 'chebitoch/about.html', {'categories': categories})