## 博客系统

### 1.[功能描述]
1. 基于ajax和auth组件实现登录验证
2. 基于ajax和forms组件实现注册功能
3. 系统首页文章列表渲染
4. 个人站点页面设计
5. 文章详情页的继承
6. 点赞与踩
7. 评论功能
8. 富文本编辑器发布文章
9. 防止xss攻击

### 2.[开发环境]
1. 操作系统：macOS10.15.7
2. 解释器版本：python3.7
3. web框架：Django3.1.1

### 3.[项目结构简介]
1. blog
   - templatetags（html模版）
   - verifyCode（验证码相关）
   - model_forms.py（初始化注册、登录相关的校验规则类）
   - models.py（初始化数据表）
   - views.py（视图函数）
2. blog_system
   - urls.py
   - settings.py
3. media（用户上传文件夹）
4. static（本地静态文件）
5. templates
   - parts（html模版）
   - base0.html
   - home.html（主页）
   - user-article.html（文章详情页）
   - user-article-create.html（新建文章）
   - user-article-change.html（修改文章）
   - user-article-manager.html（文章管理）
   - user-blog.html（个人站点）
6. manage.py

### 4.[第三方库]
1. Pillow
2. bs4

### 5.[启动方式]
1. 开启mysql数据库
    * 创建一个新库以存放表
    ```mysql
    create database db_blog;
    ```
    * 修改对应setting.py数据库连接配置
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_blog',  # 数据库名
            'USER': '****',  # mysql账号
            'PASSWORD': '******',  # mysql密码
            'HOST': '127.0.0.1',
            'PORT': 3306
        }
    }
    ```
2. 终端运行以下指令，生成表结构
```
python3 manage.py makemigrations
python3 manage.py migrate
```
3. 启动方式一：终端
```
python3 manage.py runserver 127.0.0.1:8080
```
4. 启动方式二：IDE
    * pycharm直接运行
5. 浏览器输入对应IP
    * http://127.0.0.1:8080/
    
### 6.[用户登录信息]
1. 进入首页即可注册账号、密码

### 7.[运行效果]
1. 系统首页
![ec3dbbf5424a38cd15698ec5cac778d9](README.resources/A148786C-C530-4244-879B-08743C32EE35.png)
2. 个人站点
![a3efe9ec214dfaf78de8c605438ef168](README.resources/21BA701D-4ADE-449D-9B36-2193D875A96C.png)
3. 文章管理
![3874dc644ac68eb56f266ebf5d1864e6](README.resources/image-20201102224538694.png)
4. 文章发布
![b20bf3660cd74d65f10669ef9eb89368](README.resources/image-20201102224639839.png)
5. 文章详情页
![43754602d6e1efee67f415bf01ae60e9](README.resources/image-20201102224845671.png)
6. 文章点赞及评论
![3532263dfdcf29e3c6c14843ad400656](README.resources/image-20201102230526241.png)
![b65cf299c989f215d551e70ec158a5c6](README.resources/image-20201102230355713.png)




