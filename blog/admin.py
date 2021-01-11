from django.contrib import admin

# todo:注册admin
from blog import models
admin.site.register(models.UserInfo)
admin.site.register(models.BlogSite)
admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.register(models.ArticleLike)
admin.site.register(models.Comment)
