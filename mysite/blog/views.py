from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, Book
from django.contrib.postgres.search import TrigramSimilarity
from .forms import CommentForm, SearchForm
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.db.models import Q


# Create your views here.

# Main page
def index(request):

    books = Book.published.order_by('-publish')[:4]
    latest_posts = Post.published.order_by('-publish')[:4]
    return render(request, 'index.html', {'latest_posts': latest_posts, 'books': books})

# Blog section
def post_list(request, tag_slug=None):
    
    post_list = Post.published.all()
    tags = Tag.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination
    paginator = Paginator(post_list, 8)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # page num not an int
        posts = paginator.page(1)
    except EmptyPage:
        # page num out-of-range
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag, 'tags': tags})

def post_detail(request, post):

    post = get_object_or_404(Post, 
                            status=Post.Status.PUBLISHED, 
                            slug=post)

    # list active comments
    comments = post.comments.filter(active=True)
    # comments form
    form = CommentForm()

    # similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None

    # comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})


def post_search(request):

    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})

# Books section
def books(request, tag_slug=None):

    books = Book.objects.all()
    tags = Tag.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        books = books.filter(tags__in=[tag])

    return render(request, 'books/books.html', {'books': books, "tags": tags})

# Projects section
def projects(request):
    
    return render(request, 'projects/projects.html')

# Learning section
def learning(request):
    
    return render(request, 'learning/learning.html')

# SEARCH VIEWS
def search_books(request):
    
    query = request.POST.get('query')
    queryset = Book.published.filter(Q(title__icontains=query)|Q(tags__name__icontains=query)).distinct()
    
    if queryset:
        return render(request, 'books/search.html', {'books': queryset})
    else:
        return HttpResponse('')
    
def search_blog(request):
    
    query = request.POST.get('query')
    queryset = Post.published.filter(Q(title__icontains=query)|Q(tags__name__icontains=query)|Q(topics__name__icontains=query)).distinct()
    
    if queryset:
        return render(request, 'blog/post/search.html', {'posts': queryset})
    else:
        return HttpResponse('')

def blog_tags(request, tag_slug=None):
    
    post_list = Post.published.all()
    tags = Tag.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
        return render(request, 'blog/post/search.html', {'posts': post_list})
    else:
        return HttpResponse('')