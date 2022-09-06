from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.all_blogs, name='all_blogs'),
    path('<int:blog_id>/', views.detail, name='detail'),
    path('best_blogs', views.best_blogs, name='best_blogs'),
    path('search', views.search, name='search'),
    path('blog_csv', views.blog_csv, name='blog_csv'),    
    path('tag/<slug:tag_slug>', views.all_blogs, name='blog_by_tag')    
]