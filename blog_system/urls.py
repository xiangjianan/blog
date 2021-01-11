"""blog_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve  # todo:media配置

from blog_system import settings
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # todo:media配置
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    # 主页
    path('', views.home),
    path('home/', views.home),
    # 注册、登录
    path('logout/', views.logout),
    path('login/', views.login),
    path('reg/', views.reg),
    path('verify_code/', views.verify_code),
    # 点赞、评论
    path('article_like/', views.article_like),
    path('article_comment/', views.article_comment),
    path('article_comment_tree/', views.article_comment_tree),
    # 个人站点
    path('change_site_title/', views.change_site_title),
    re_path(r'^(?P<username>\w+)/$', views.user_blog),
    re_path(r'^(?P<username>\w+)/(?P<condition>tag|category|time)/(?P<param>.*)/$', views.user_blog),
    # 文章
    re_path(r'^(?P<username>\w+)/articles/(?P<article_id>\d+)/$', views.user_article),
    # 文章管理
    re_path(r'^(?P<username>\w+)/article_manager/$', views.user_article_manager),
    re_path(r'^(?P<username>\w+)/article_manager/article_create/$', views.article_create),
    re_path(r'^(?P<username>\w+)/article_manager/article_change/(?P<article_id>\d+)/$', views.article_change),
    re_path(r'^(?P<username>\w+)/article_manager/article_delete/(?P<article_id>\d+)/$', views.article_delete),
]
