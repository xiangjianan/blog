from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import F
from django.db import transaction
from django.contrib import auth  # auth组件
from django.core.paginator import Paginator, EmptyPage  # 分页器

import json
from bs4 import BeautifulSoup

from blog.model_forms import *  # forms组件
from blog.models import *  # 表
from blog.verifyCode.getVerifyCode import get_verify_code_img  # 验证码


def my_paginator(request, article_list, max_item):
    """ 文章分页 """
    paginator = Paginator(article_list, max_item)
    current_page_num = int(request.GET.get('page', 1))
    try:  # 正常页码
        current_page = paginator.page(current_page_num)
    except EmptyPage as e:  # 错误页码，设置为1
        current_page = paginator.page(1)
    num = 3  # 显示的页面总个数：(num * 2) + 1
    if paginator.num_pages > (num * 2) + 1:
        if current_page_num - num <= 0:
            page_range = range(1, (num * 2) + 2)
        elif current_page_num + num > paginator.count:
            page_range = range(paginator.count - (num * 2), paginator.count + 1)
        else:
            page_range = range(current_page_num - num, current_page_num + num + 1)
    else:
        page_range = paginator.page_range
    return current_page, page_range, current_page_num


def home(request):
    """ 主页 """
    # 欢迎页
    if not request.session.get('welcome'):
        request.session['welcome'] = 'first'
    else:
        request.session['welcome'] = 'again'
    # 文章分页
    article_list = Article.objects.all().order_by('-create_time')
    current_page, page_range, current_page_num = my_paginator(request, article_list, 5)
    # forms组件
    form_login = UserFormLogin()
    form_reg = UserFormReg()
    return render(request, "home.html", locals())


def logout(request):
    """ 登出 """
    auth.logout(request)
    return redirect('/home/')


def login(request):
    """ 登录 """
    if request.is_ajax():
        res = {'user': None, 'msg': None}
        # 校验：验证码
        verify_code_str = request.session.get('verify_code_str')
        verify_code_str_login = request.POST.get('verify_code_str_login')
        if verify_code_str.upper() == verify_code_str_login.upper():
            # 校验：表单格式
            form_login = UserFormLogin(request.POST)
            if form_login.is_valid():
                # 校验：用户密码
                username = form_login.cleaned_data.get('username_login')
                password = form_login.cleaned_data.get('password_login')
                obj = auth.authenticate(username=username, password=password)
                if obj:
                    auth.login(request, obj)
                    res['user'] = str(obj)
                else:
                    res['msg'] = {'user-pwd-login': ['用户名或密码错误']}
            else:
                res['msg'] = form_login.errors
        else:
            res['msg'] = {'verify-code-str-login': ['验证码错误']}
        return JsonResponse(res)


def reg(request):
    """ 注册 """
    if request.is_ajax():
        res = {'user': None, 'msg': None}
        # 校验：验证码
        verify_code_str = request.session.get('verify_code_str')
        verify_code_str_reg = request.POST.get('verify_code_str_reg')
        if verify_code_str.upper() == verify_code_str_reg.upper():
            # 校验：表单格式
            form_reg = UserFormReg(request.POST)
            if form_reg.is_valid():
                res['user'] = form_reg.cleaned_data.get('username_reg')
                username = form_reg.cleaned_data.get('username_reg')
                password = form_reg.cleaned_data.get('password_reg')
                email = form_reg.cleaned_data.get('email_reg')
                avatar = request.FILES.get('avatar_reg')
                extra = {}
                if avatar:
                    extra['avatar'] = avatar
                # 生成站点表记录
                blog_site = BlogSite.objects.create(title=username + '的个人站点')
                # 生成用户表记录
                UserInfo.objects.create_user(username=username, password=password, email=email, blog_site=blog_site,
                                             **extra)
            else:
                res['msg'] = form_reg.errors
        else:
            res['msg'] = {'verify-code-str-reg': ['验证码错误']}
        return JsonResponse(res)


def verify_code(request):
    """ 获取验证码图片对象 """
    image_obj = get_verify_code_img(request)
    return HttpResponse(image_obj)


def user_blog(request, username, **kwargs):
    """ 个人站点 """
    user = UserInfo.objects.filter(username=username).first()
    if not user:
        return render(request, "404.html")
    else:
        blog_site = user.blog_site
        article_list = Article.objects.filter(user=user).order_by('-create_time')
        # 判断是否进入标签或每月文章
        if kwargs:
            condition = kwargs.get('condition')
            param = kwargs.get('param')
            # 文章标签
            if condition == 'tag':
                article_list = article_list.filter(tag__title=param).order_by('-create_time')
            # 每月文章
            else:
                y, m = param.split('-')
                article_list = article_list.filter(create_time__year=y, create_time__month=m).order_by('-create_time')
        # 分页
        current_page, page_range, current_page_num = my_paginator(request, article_list, 5)
        return render(request, "user-blog.html", locals())


def user_article(request, username, article_id):
    """ 文章详情页 """
    article = Article.objects.filter(pk=article_id).first()
    if article:
        # 文章阅读数+1
        Article.objects.filter(pk=article_id).update(view_count=F('view_count') + 1)
        # 当前文章评论列表
        comment_list = Comment.objects.filter(article_id=article_id)
        # 文章修改前信息
        tag_obj = Tag.objects.filter(article=article)
        tag_list = []
        for tag in tag_obj:
            tag_list.append(tag.title)
        return render(request, "user-article.html", locals())
    else:
        return render(request, "404.html")


def article_like(request):
    """ 点赞 """
    if request.is_ajax():
        user_id = request.user.pk
        # 判断用户是否登录
        if user_id:
            is_like = json.loads(request.POST.get('is_like'))
            article_id = request.POST.get('article_id')
            res = {'is_success': True, 'msg': None}
            obj = ArticleLike.objects.filter(user_id=user_id, article_id=article_id).first()
            # 判断用户是否赞或踩过
            if not obj:
                ArticleLike.objects.create(user_id=user_id, article_id=article_id, is_like=is_like)
                if is_like:
                    Article.objects.filter(pk=article_id).update(like_count=F('like_count') + 1)
                else:
                    Article.objects.filter(pk=article_id).update(dislike_count=F('dislike_count') + 1)
            # 不能重复点赞
            else:
                res['is_success'] = False
                res['is_like'] = obj.is_like
        # 未登录不能点赞
        else:
            res = {'is_success': False, 'msg': '请登录'}
        return JsonResponse(res)


def article_comment(request):
    """ 发布评论 """
    if request.is_ajax():
        user_id = request.user.pk
        article_id = request.POST.get('article_id')
        content = request.POST.get('content')
        comment_parent_id = request.POST.get('comment_parent_id')
        # 事务：创建评论 + 评论数加1
        with transaction.atomic():
            comment_obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content,
                                                 comment_parent_id=comment_parent_id)
            Article.objects.filter(pk=article_id).update(comment_count=F('comment_count') + 1)
        res = {'is_success': True, 'create_time': comment_obj.create_time.strftime('%Y-%m-%d %X'),
               'user_name': request.user.username, 'comment_id': comment_obj.pk}
        return JsonResponse(res)


def article_comment_tree(request):
    """ 展示评论 """
    if request.is_ajax():
        article_id = request.POST.get('article_id')
        comment_list = list(
            Comment.objects.filter(article_id=article_id).order_by('pk').values('pk', 'content', 'comment_parent_id'))
        # 增加评论人、评论时间
        for comment in comment_list:
            comment['user_name'] = Comment.objects.filter(pk=comment['pk']).first().user.username
            comment['create_time'] = Comment.objects.filter(pk=comment['pk']).first().create_time.strftime(
                '%Y-%m-%d %X')
        return JsonResponse(comment_list, safe=False)


def user_article_manager(request, username):
    """ 文章管理 """
    article_list = Article.objects.filter(user__username=username).order_by('-create_time')
    # 分页
    current_page, page_range, current_page_num = my_paginator(request, article_list, 10)
    return render(request, 'user-article-manager.html', locals())


def article_create(request, username):
    """ 创建文章 """
    if request.method == 'POST':
        title, soup, desc, tag_obj_list = article_submit(request, username)
        # 添加文章表记录
        user_id = UserInfo.objects.filter(username=username).first().pk
        article_obj = Article.objects.create(title=title, content=str(soup), desc=desc, user_id=user_id)
        article_obj.tag.add(*tag_obj_list)
        return redirect('/' + username + '/')
    return render(request, 'user-article-create.html', locals())


def change_site_title(request):
    """ 修改个人站点标题 """
    if request.is_ajax():
        res = {'user': None, 'msg': None}
        site_title = request.POST.get('site_title')
        site_id = request.POST.get('site_id')
        BlogSite.objects.filter(pk=site_id).update(title=site_title)
        return JsonResponse(res)


def article_change(request, username, article_id):
    """ 修改文章 """
    if request.method == 'POST':
        title, soup, desc, tag_obj_list = article_submit(request, username)
        # 更新文章表记录
        Article.objects.filter(pk=article_id).update(title=title, content=str(soup), desc=desc)
        article_obj = Article.objects.filter(pk=article_id).first()
        article_obj.tag.clear()
        article_obj.tag.add(*tag_obj_list)
        return redirect('/' + username + '/article_manager/')
    # 文章修改前信息
    article_obj = Article.objects.filter(pk=article_id).first()
    tag_obj = Tag.objects.filter(article=article_obj)
    tag_list = []
    for tag in tag_obj:
        tag_list.append(tag.title)
    tags = ' '.join(tag_list)
    return render(request, 'user-article-change.html', locals())


def article_submit(request, username):
    """ 处理用户提交的文章内容 """
    title = request.POST.get('title')
    content = request.POST.get('content')
    tag_list = request.POST.get('tag').split(' ')
    tag_obj_list = []
    for tag in tag_list:
        tag_obj = Tag.objects.filter(blog_site__userinfo__username=username).filter(title=tag).first()
        if not tag_obj:
            blog_site_obj = BlogSite.objects.filter(userinfo__username=username).first()
            tag_obj = Tag.objects.create(title=tag, blog_site=blog_site_obj)
        tag_obj_list.append(tag_obj)
    soup = BeautifulSoup(content, 'html.parser')
    # 防止xss攻击
    for tag in soup.find_all():
        if tag.name == 'script':
            tag.decompose()
    desc = soup.text[0:255]
    return title, soup, desc, tag_obj_list


def article_delete(request, username, article_id):
    """ 删除文章 """
    # 如果标签只有最后一篇文章，则删除该标签
    tags = Tag.objects.filter(article__pk=article_id)
    for tag in tags:
        if Article.objects.filter(tag=tag).count() == 1:
            Tag.objects.filter(title=tag.title).delete()
    # 删除文章
    Article.objects.filter(pk=article_id).delete()
    return redirect('/' + username + '/article_manager/')
