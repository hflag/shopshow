             第一章 项目创建

一、创建项目的虚拟环境
1. 在D：盘根目录下创建一个新的文件夹‘www'，该文件夹用于寄存我们创建的shopshow项目。
2. 打开cmd终端，导航到文件夹’www‘下，创建虚拟环境webvenv，使用如下命令：
    python -m venv webvenv
3. 激活虚拟环境，在当前路径下输入如下命令激活新创建的虚拟环境：
    d:\www>webvenv\scripts\activate
此时，如果命令行提示显示为：<webvenv> d:\www 就表示虚拟环境已经处于激活状态。
4. 安装django框架。在虚拟环境中，输入如下命令：
    <webvenv> d:\www> pip install django
一旦django安装完毕，那么我们的开发环境也就安装完成了。

二、创建shopshow项目
1. 打开pycharm，选择’创建项目‘(django项目）
2. 项目位置要选择上一步创建的www文件夹中，名字为shopshow
3. 项目的解释器选择新建的虚拟环境中的python.exe
4. 将项目模板文件夹清空。点击创建即可完成项目创建。

三、在shopshow中添加应用shop
1. 打开pycharm的Terminal
2. 通过下面的命令创建应用
    python manage.py startapp shop
3. 添加应用到项目中，打开项目下的settings.py文件，找到
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    在后面添加新建的应用shop：
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'shop',
    ]


            第二章 项目中集成bootstrap

bootstrap作为前端开发框架，其牛气自不必说了。主要看如何往我们的项目shopshow里集成。bootstrap官网下载其最新版本
将需要的css和js全部放入应用shop的static文件夹下。另外为了使用jQuery，这里也顺便集成了jQuery。

悄悄告诉你，如果你想省事，可以直接拷贝、粘贴我这里的static目录，放入项目中，一下搞定：）

关于bootstrap的使用要和django的模板使用紧密结合起来，强强联合，发挥二者的作用，为此我们在shop应用下添加‘templates/shop/product'
文件夹，在shop文件夹中（不要搞错了）新建一个模板文件base.html.这个文件参考了bootstrap官网提供的模板，并且结合了
django的模板语言，不得不说是强强联合了，哈哈哈！

base.html代码如下：
<!DOCTYPE html>
{% load static %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{% static "bootstrap-4.1.1/dist/css/bootstrap.min.css" %}">
    <link rel="stylesheet" href="{% static "font-awesome-4.7.0/css/font-awesome.min.css" %}">
    <link rel="stylesheet" href="{% static "bootstrap-social-gh-pages/bootstrap-social.css" %}">
    <script src="{% static 'js/jquery-3.3.1.min.js' %}"></script>
    {% block custom_css %}{% endblock %}
</head>
<body >
    {% block content %}
    {% endblock %}
<script src="{% static "js/jquery-3.3.1.min.js" %}"></script>
<script src="{% static "js/popper.min.js" %}"></script>
<script src="{% static "bootstrap-4.1.1/dist/js/bootstrap.min.js" %}"></script>
</body>
</html>
其中的html标签自不必说了，{%...%}就是django的模板语言，如果不懂参考django的文档。接下来，我们先来填充一些数据，
以便我们的前台页面显示。


                第三章 建立数据模型

为了方便用户浏览商品，我们打算建立一个产品分类表-Category， 一个产品表-Product。
在django里完全采用ORM，也就是对象关系映射机制，每个模型类对应数据库中的一张表，而类的属性对应表中的字段。
一、建立数据模型
代码如下：

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock =models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

因为Product中使用了ImageField，所以必须安装第三方图像处理库pillow，在Terminal中使用如下命令安装：
(webvenv) F:\www\shopshow>pip install pillow

同时，为了是页面能够正常解析图片，需要修改settings.py，添加如下代码：
# for media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

然后在项目shopshow的urls中修改：

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

二、将数据模型注册在admin中
1. 找到shop应用中的admin.py文件，打开后写入下面的代码：

from django.contrib import admin

from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)

三、迁移数据库
在django中，一旦修改了应用的models，那么必须使用如下2条命令完成数据库的迁移：
1. python manage.py makemigrations shop
2. python manage.py migrate shop
为了能够访问admin页面，我们创建一个超级用户，通过如下命令
 python manage.py createsuperuser
根据提示输入用户名、邮箱和密码，完成创建。

接下来就可以启动服务器，在浏览器地址栏输入localhost:8000/admin/进入admin页面，找到category和product，分别添加
适当数据，以便我们后面页面开发使用。