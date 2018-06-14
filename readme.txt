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


                第四章 创建产品分类视图

django项目下任何一个应用都会有一个views.py的文件，这里就是建立视图的地方。视图就是我们主要业务逻辑
处理的位置。

一、创建需要的视图
django中视图可以使用类视图，也可以使用函数视图，某些情况下，二者可以相互替代。但是相对来说使用
类视图更加灵活，功能也更强大，在目前shop视图中，我们采用类视图。

1. 为了显示产品分类，我们需要创建一个所有产品的列表视图，当然该视图也可以是某个类别的所有产品，编辑
views.py添加如下代码：

from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View

from .models import Category, Product


class ProductsView(View):
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        return render(request, 'shop/product/list.html', {'category': category,
                                                          'categories': categories,
                                                          'products': products})

2. 同时我们也需要一个提取和显示一件产品的视图，在views.py中继续添加下面的代码：

class ProductView(View):
    def get(self, request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug)
        return render(request, 'shop/product/detail.html', {'product': product})

二、 为应用编写路由
关于路由编写的策略，我们对每个应用编写一个自己的路由，然后聚合到项目路由，这样构成总路由包含分支路由的关系，以便
维护。
1. 在应用shop下创建一个urls.py的文件，写入下面的内容：

from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.ProductsView.as_view(), name='product_list'),
    path('<str:category_slug>/', views.ProductsView.as_view(), name='product_list_by_category'),
    path('<int:id>/<str:slug>/', views.ProductView.as_view(), name='product_detail'),
]
2. 把shop的路由添加到项目路由文件中，修改shopshow中的urls.py如下：

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

三、 进一步完善模型
为了方便回去特定类别商品的url以及具体某件商品的url我们在模型中添加如下两个函数：

from django.urls import reverse


class Category(models.Model):
    ...

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    ...

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


                第五章 创建显示产品的页面

在shop应用下的templates/shop/product文件下依次创建list.html和detail.html。分别用于显示
产品列表页面和商品详情页面。

一、 商品列表页面，该页面使用了django模板继承的机制，也即使通过{% extends "shop/base-4.1.1.html" %}
完成页面继承的。另外其中使用了bootstrap网格布局，在bootstrap4中开始默认使用flexbox功能，给页面
布局带来了很多方便。list.html代码如下：

{% extends "shop/base-4.1.1.html" %}
{% load static %}

{% block custom_css %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
{% endblock %}

{% block title %}
    {% if category %}{{ category.name }}{% else %}Products{% endif %}
{% endblock %}

{% block content %}
    <nav class="navbar navbar-expand-sm navbar-dark bg-primary ">
        <div class="container">
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#Navbar">
                <span class="navbar-toggler-icon"></span>
            </button>
            <a class="navbar-brand" href="/">Shop show</a>
            <div class="collapse navbar-collapse" id="Navbar">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <a class="nav-link" href="{% url 'shop:product_list' %}">
                            <span class="fa fa-home fa-lg"></span>
                            Home
                        </a>
                    </li>

                </ul>
            </div>
        </div>
    </nav>
    <header class="jumbotron" style="padding: 0;">
        <div class="container">
            <div class="row justify-content-end">
                <div style="margin: 10px">
                    Your cart is empty.
                </div>
            </div>
        </div>
    </header>
    <div class="container">
        <div class="row row-content ">
            <div class="col-12 col-sm-2 ">
                <h3>商品类别</h3>
                <ul id="sidermenu" class="nav flex-column">
                  <li {% if not category %}class="nav-item active"{% else %}class="nav-item"{% endif %}>
                    <a class="nav-link " href="{% url 'shop:product_list' %}">所有</a>
                  </li>
                {% for c in categories %}
                  <li {% if category.slug == c.slug %}class="nav-item active"{% else %}class="nav-item"{% endif %}>
                    <a class="nav-link" href="{{ c.get_absolute_url }}">{{ c.name }}</a>
                  </li>
                {% endfor %}
                </ul>
            </div>
            <div class="col-12 col-sm ">
                <h2>{% if category %}{{ category.name }}{% else %}全部商品{% endif %}</h2>
                <div class="row">
                    {% for product in products %}
                        <div class="col-12 col-sm-3">
                            <div class="item" style="text-align:center;">
                                <a href="{{ product.get_absolute_url }}">
                                    <img src="{{ product.image.url }} " style='width:100%'>
                                </a>
                                <a href="{{ product.get_absolute_url }}">{{ product.name }}</a><br>
                                ${{ product.price }}
                            </div>

                        </div>
                    {% endfor %}

                </div>
            </div>
        </div>
        # 分页功能区
    </div>
{% endblock %}

二、商品详情页面，通用也继承自继承模板，而且采用了bootstrap的网格布局。代码如下：

{% extends "shop/base-4.1.1.html" %}
{% load static %}

{% block custom_css %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
{% endblock %}

{% block title %}
    {% if category %}{{ category.title }}{% else %}Products{% endif %}
{% endblock %}

{% block content %}
    <nav class="navbar navbar-expand-sm navbar-dark bg-primary ">
        <div class="container">
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#Navbar">
                <span class="navbar-toggler-icon"></span>
            </button>
            <a class="navbar-brand" href="/">Shop show</a>
            <div class="collapse navbar-collapse" id="Navbar">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item ">
                        <a class="nav-link" href="{% url 'shop:product_list' %}">
                            <span class="fa fa-home fa-lg"></span>
                            Home
                        </a>
                    </li>

                </ul>
            </div>
        </div>
    </nav>
    <header class="jumbotron" style="padding: 0;">
        <div class="container">
            <div class="row justify-content-end">
                <div style="margin: 10px">
                    Your cart is empty.
                </div>
            </div>
        </div>
    </header>
    <div class="container">
        <div class="row">
            <div class="col-12 col-sm-4 " >
                <img src="{{ product.image.url }}" width="100%">
            </div>
            <div class="col-12 col-sm-8">
                <h1>{{ product.name }}</h1>
                <h2>
                    <a href="{{ product.category.get_absolute_url }}">
                        {{ product.category }}
                    </a>
                </h2>
                <p class="price">${{ product.price }}</p>

                {{ product.description|linebreaks }}
            </div>
        </div>
    </div>
{% endblock %}

关于django模板，如果我们把上面两个页面代码折叠后，看上去如下：
{% extends "shop/base-4.1.1.html" %}
{% load static %}

{% block custom_css %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
{% endblock %}

{% block title %}
    {% if category %}{{ category.name }}{% else %}Products{% endif %}
{% endblock %}

{% block content %}
    ...
{% endblock %}

也就是说上面list和detail页面都有上面的骨架，只是具体内容不同了，而相同的部分都被写入了base页面，这里
就节省了很多重复的代码，这就是模板继承的好处！