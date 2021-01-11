from django import template
from django.db.models import Count
from django.db.models.functions import TruncMonth
from blog.models import *
from blog.model_forms import *

register = template.Library()


# todo:inclusion_tag
@register.inclusion_tag('parts/side-left.html')
def get_side_left_style(request, username):
    user = UserInfo.objects.filter(username=username).first()
    # 站点
    blog_site = user.blog_site
    # 文章排行
    article_list_hot = Article.objects.filter(user__username=username).order_by('-view_count')[:5]
    # 当前站点每个标签下的文章
    tag_list = Tag.objects.filter(blog_site=blog_site).values('pk').annotate(
        c=Count('article__title')).values('title', 'c')
    # 当前站点每月下的文章
    time_list = Article.objects.filter(user=user).annotate(
        y_m_time=TruncMonth('create_time')).values('y_m_time').annotate(
        c=Count("id")).values('y_m_time', 'c')
    return {'username': username, 'blog_site': blog_site, 'tag_list': tag_list, 'article_list_hot': article_list_hot,
            'time_list': time_list, 'request': request}


@register.inclusion_tag('parts/side-right.html')
def get_side_right_style(request):
    # 文章推荐
    article_list_hot = Article.objects.order_by('-like_count')[:10]
    article_list_view = Article.objects.order_by('-view_count')[:10]
    return {'article_list_hot': article_list_hot, 'article_list_view': article_list_view, 'request': request}


@register.inclusion_tag('parts/header.html')
def get_header_style(request):
    form_login = UserFormLogin()
    form_reg = UserFormReg()
    username = UserInfo.objects.filter(username=request.user.username).first()
    blog_site = BlogSite.objects.filter(userinfo=username).first()
    return {'form_login': form_login, 'form_reg': form_reg, 'request': request, 'blog_site': blog_site}


@register.inclusion_tag('parts/paginator.html')
def get_paginator_style(current_page, page_range, current_page_num):
    return {'current_page': current_page, 'page_range': page_range, 'current_page_num': current_page_num}


@register.inclusion_tag('parts/side-left-manager.html')
def get_side_left_manager_style(request, username):
    blog_site = BlogSite.objects.filter(userinfo__username=username).first()
    return {'request': request, 'username': username, 'blog_site': blog_site}
