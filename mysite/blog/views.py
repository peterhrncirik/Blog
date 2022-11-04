from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.views.decorators.http import require_POST


# Create your views here.
class PostListView(ListView):

    """
    Alternative post list view
    """

    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.xhtml'


def post_list(request):
    
    post_list = Post.published.all()

    # Pagination
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # page num not an int
        posts = paginator.page(1)
    except EmptyPage:
        # page num out-of-range
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.xhtml', {'posts': posts})

def post_detail(request, year, month, day, post):

    post = get_object_or_404(Post, 
                            status=Post.Status.PUBLISHED, 
                            slug=post,
                            publish__year=year, 
                            publish__month=month, 
                            publish__day=day)

    # list active comments
    comments = post.comments.filter(active=True)
    # comments form
    form = CommentForm()

    return render(request, 'blog/post/detail.xhtml', {'post': post, 'comments': comments, 'form': form})

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
    return render(request, 'blog/post/comment.xhtml', {'post': post, 'form': form, 'comment': comment})