from os import name
from django.urls import path, include
from .views import ArticlePreview, AuthorList, CategoryListView, ArticleListView, ArticleDetailView


app_name = 'blog'
urlpatterns = [
    path('', ArticleListView.as_view(), name='index'),
    path('page/<int:page>', ArticleListView.as_view(), name='index'),
    path('article/<slug:slug>', ArticleDetailView.as_view(), name='detail'),
    path('preview/<int:pk>', ArticlePreview.as_view(), name='preview'),
    path('category/<slug:slug>', CategoryListView.as_view(), name='category'),
    path('category/<slug:slug>/page/<int:page>', CategoryListView.as_view(), name='category'),
    path('author/<slug:username>', AuthorList.as_view(), name='author'),
    path('author/<slug:username>/page/<int:page>', AuthorList.as_view(), name='author'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
