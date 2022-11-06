from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Main
    path('', views.index, name='index'),

    # Blog
    path('blog/', views.post_list, name='blog'),
    path('blog/tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('blog/<int:post_id>/comment/', views.post_comment, name='post_comment'),

    # Search
    path('search/', views.post_search, name='post_search'),

    # Books
]