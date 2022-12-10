from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Main
    path('', views.index, name='index'),

    # Blog
    path('blog/', views.post_list, name='blog'),
    path('blog/tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('blog/<slug:post>/', views.post_detail, name='post_detail'),
    path('blog/<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('search-blog/', views.search_blog, name='search_blog'),

    # Search
    path('search/', views.post_search, name='post_search'),

    # Books
   path('books/', views.books, name='books'),
#    path('book/<slug:book>/', views.book_detail, name='book_detail'),
   path('search-books/', views.search_books, name='search_books'),
   
   # Projects
   path('projects/', views.projects, name='projects'),
   
   # Projects
   path('learning/', views.learning, name='learning'),
]