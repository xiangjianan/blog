from django.db import models

from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户信息表（自定义的auth组件）：
    用户名｜密码｜邮箱｜创建时间｜头像文件｜关联blog
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='用户创建时间')
    avatar = models.FileField(upload_to='avatars/', default='avatars/default.png')
    # 关系表
    blog_site = models.OneToOneField('BlogSite', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class BlogSite(models.Model):
    """
    用户站点表：
    站点标题
    """
    title = models.CharField(max_length=32, null=True, verbose_name='个人站点标题')

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    文章标签表：
    标题｜用户站点（一对多）
    """
    title = models.CharField(max_length=32, verbose_name='文章标签标题')
    # 关系表
    blog_site = models.ForeignKey('BlogSite', on_delete=models.CASCADE, verbose_name='所属的用户站点')

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    文章表：
    标题｜描述信息｜创建时间｜内容｜访问量｜点赞数｜反对数｜评论数｜作者｜标签
    """
    title = models.CharField(max_length=64, verbose_name='文章标题')
    desc = models.CharField(max_length=256, verbose_name='文章描述信息')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='文章创建日期')
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    # 关系表
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class ArticleLike(models.Model):
    """
    点赞表：
    点赞人｜点赞文章｜点赞状态
    """
    is_like = models.BooleanField(default=True)
    # 关系表
    user = models.ForeignKey('UserInfo', null=True, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', null=True, on_delete=models.CASCADE)


class Comment(models.Model):
    """
    评论表：
    评论人｜评论文章｜评论内容｜评论时间｜父级评论
    """
    user = models.ForeignKey('UserInfo', null=True, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', null=True, on_delete=models.CASCADE)
    content = models.CharField(max_length=256, verbose_name='评论内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    # 关系表：自关联
    comment_parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
