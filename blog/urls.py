from django.contrib import admin
from django.urls import path
from blog import views
from django.conf.urls import url

app_name = 'blog'

urlpatterns = [
    path('index/', views.Index.as_view(), name='index'),
    url(r'article/(?P<article_id>\d+)+', views.Detail.as_view(), name='article'),
    url(r'tag/(?P<tag_id>\d+)+', views.Tag.as_view(), name='tag'),
    url(r'about/', views.About.as_view(), name='about'),
]