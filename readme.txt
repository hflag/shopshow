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

                第六章 为产品列表页添加分页功能

分页功能是很多页面所必须的一个组件，试想一下我们的产品有成百上千件，那么显示在一个页面是很难受的。django
本身内置有分页的功能，在这里我们想结合bootstrap和django来显示分页功能，为此我们使用一个第三方分页应用：
django-pure-pagination, 可以在github上搜素该应用，结合其文档进行安装和使用。

一、安装和设置django-pure-pagination
1. 安装根据其文档，在pycharm的Terminal中输入如下命令进行安装
    pip install pip install django-pure-pagination

2. 在项目settings.py中添加 pure_pagination,找到INSTALLED_APPS，添加如下代码：
    INSTALLED_APPS = (
    ...
    'pure_pagination',
)

二、修改views.py添加分页功能
其中修改代码如下：

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class ProductsView(View):
    def get(self, request, category_slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.filter(available=True)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = products.filter(category=category)

        # 商品分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 每页设定为8件商品
        p = Paginator(products, 8, request=request)

        perpage_products = p.page(page)

        return render(request, 'shop/product/list.html', {'category': category,
                                                          'categories': categories,
                                                          'products': perpage_products})


三、修改list.html页面添加分页显示
需要修改的代码如下：

            <div class="col-12 col-sm ">
                <h2>{% if category %}{{ category.name }}{% else %}全部商品{% endif %}</h2>
                <div class="row">
                    {% for product in products.object_list %}
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
                <!-- 分页组件 -->
                <nav class="row mt-3 justify-content-center" aria-label="Page navigation example">
                  <ul class="pagination">
                      {% if products.has_previous %}
                        <li class="page-item"><a class="page-link" href="?{{ products.previous_page_number.querystring }}">上一页</a></li>
                      {% endif %}

                      {% for page in products.pages %}
                          {% if page %}
                              {% ifequal page products.number %}
                                  <li class="page-item active"><a class="page-link" href="?{{ page.querystring }}">{{ page }}</a></li>
                              {% else %}
                                  <li class="page-item"><a class="page-link" href="?{{ page.querystring }}">{{ page }}</a></li>
                              {% endifequal %}
                          {% else %}
                              <li class="none"><a href="">...</a> </li>
                          {% endif %}
                      {% endfor %}

                      {% if products.has_next %}
                          <li class="page-item"><a class="page-link" href="?{{ page_obj.next_page_number.querystring }}">下一页</a></li>
                      {% endif %}
                  </ul>
                </nav>
            </div>

注意：这里前端采用了bootstrap的分页组件nav


                        第七章 购物车

当我们有了商品展示页面后，就需要创建一个购物车允许用户选择他们希望购买的商品。购物车是一个用户暂存他们想要
的商品的地方，因此用户访问网站期间，购物车必须保存在session中。

我们将使用Django的session框架来保存购物车。购物车一直保存在session中，直到用户完成购买或支付。

为了使用session，必须项目中的MIDDLEWARE_CLASSES设置为'django.contrib.sessions.middleware.SessionMiddleware'.
这个中间层用来管理session，并且创建项目时，默认已经添加。

一、session中存储购物车
我们需要一个简单的数据结构便于序列化为JSON格式在session中存储购物车里的商品。购物车里的每件商品，购物车必须
包含下列数据：
    * 一件商品的id
    * 这件商品的数量
    * 商品的单价

接下来就是必须能够控制创建的购物车与session关联起来。购物车必须像下面所述的工作：
    * 一旦需要购物车，我们就检查用户的session key是否设置了。如果session中没有cart的设置，
    我们就创建一个新的cart并且保存在session中。
    * 对连续的请求，我们执行相同的检查，并且从cart session key中获取购物车中的商品。购物车里的
    商品是从session中获取，而与之相关的商品对象还是要从数据库获取。

具体来说，首先我们要编辑项目settings.py文件，添加如下代码：
    CART_SESSION_ID = 'cart'

这就是在用户session中存储购物车的关键字（key）。

二、 创建第二个应用cart，用来管理购物车

1. 打开pycharm的Terminal，输入下面命令创建应用cart：
    (webvenv) F:\www\shopshow>python manage.py startapp cart

2. 将该应用添加到项目shopshow，打开项目中的settings.py，将‘cart’添加到INSTALLED_APPS ：

    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'pure_pagination',
    'cart',
    ]

三、 创建购物车类Cart

1. 在应用cart下，添加cart.py文件
2. 输入如下代码，创建Cart类：

from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart:
    '''
    购物车类
    '''
    def __init__(self, request):
        '''
        初始化购物车
        :param request: 将购物车与session关联
        '''

        # 添加一个实例属性session，便于类里其他方法访问session
        self.session = request.session

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart: # 代表session中么有cart这个key，也就是session没有存储购物车相关信息
            cart = self.session[settings.CART_SESSION_ID] = {}

        # 再添加一个实例属性
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        '''添加商品到购物车，或者更新商品数量
        '''
        product_id = str(product.id) # 因为JSON的key值只能为字符串
        if product_id not in self.cart: # cart为一个字典类型，self.cart返回字典的key列表
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}

        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()

    def save(self):
        # 更新session中的cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # 标记session为’modified',会自动存储
        self.session.modified = True

    def remove(self, product):
        '''从购物车移去一件商品
        '''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        '''迭代购物车中的每一个元素，
        并且从数据库中获取相应的商品。
        '''
        # 获取购物车中所有元素的id
        product_ids = self.cart.keys()

        # 查询数据库，提取相应的商品对象
        products = Product.objects.filter(id__in=product_ids)

        # 把商品对象也加入购物车
        for product in products:
            self.cart[str(product.id)]['product'] = product

        # 构造一个生成器
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        '''
        数出购物车中所有的元素
        :return: 购物车商品总数
        '''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # 删除session中的购物车
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

四、购物车显示页面
    一旦用户将商品添加到购物车后，我们需要构建一个页面来显示。在应用cart下，添加购物车显示页面detail.html.其主要
代码如下：
   <div class="container">
        <h1>Your shopping cart</h1>
        {% if cart|length > 0 %}
        <div class="row">
            <div class="col-12">
                <table class="table table-borderless table-responsive-sm">
                    <thead>
                    <tr class="table-active">
                        <th scope="col">Image</th>
                        <th scope="col">Product</th>
                        <th scope="col">Quantity</th>
                        <th scope="col">Remove</th>
                        <th scope="col">Unit price</th>
                        <th scope="col">Price</th>
                    </tr>
                    </thead>
                    <tbody>
                    {% for item in cart %}
                        {% with product=item.product %}
                            <tr>
                                <td style="vertical-align: middle">
                                    <a href="{{ product.get_absolute_url }}">
                                        <img src="{{ product.image.url }}" class="img-thumbnail" width="100" height="100">
                                    </a>
                                </td>
                                <td style="vertical-align: middle">{{ product.name }}</td>
                                <td style="vertical-align: middle">
                                    <form action="{% url 'cart:cart_add' product.id %}" method="post">
                                        {{ item.update_quantity_form.quantity }}
                                        {{ item.update_quantity_form.update }}
                                        <input type="submit" class="btn btn-primary btn-sm" value="Update">
                                        {% csrf_token %}
                                    </form>
                                </td>
                                <td style="vertical-align: middle">
                                    <a href="{% url 'cart:cart_remove' product.id %}">Remove</a>
                                </td>
                                <td style="vertical-align: middle">${{ item.price }}</td>
                                <td style="vertical-align: middle">${{ item.total_price }}</td>
                            </tr>
                        {% endwith %}
                    {% endfor %}
                        <tr class="table-active">
                            <td><strong>Total</strong></td>
                            <td colspan="4"></td>
                            <td><strong>${{ cart.get_total_price }}</strong></td>
                        </tr>
                    </tbody>
                </table>
                <p class="text-right">
                    <a class="btn btn-light" href="{% url 'shop:product_list' %}">Continue shopping</a>
                    <a href="#" class="btn btn-primary">Checkout</a>
                </p>
            </div>
        </div>
        {% else %}
        <h2>Blank! Blank! Go up!</h2>
        {% endif %}
    </div>
   这里主要使用了bootstrap的table组件。

五、为购物车添加上下文处理器
    一个上下文处理器就是一个Python函数，有一个request作为参数，返回一个字典。这样在模板中
任何需要的时候，都可以取出使用。
1. 在cart应用下创建一个文件context_processors.py。添加如下代码：
from .cart import Cart

def cart(request):
    return {'cart': Cart(request)}

2. 编辑项目settings.py ,将'cart.context_processors.cart'添加到context_processors选项中。
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]
3. 修改每个页面中jumbotron中cart部分：
    <header class="jumbotron" style="padding: 0;">
        <div class="container">
            <div class="row justify-content-end">
                <div style="margin: 10px">
                    {% with total_items=cart|length %}
                        {% if cart|length > 0 %}
                            Your cart:
                            <a href="{% url 'cart:cart_detail' %}">
                                {{ total_items }} item{{ total_items|pluralize }},
                                ${{ cart.get_total_price }}
                            </a>
                        {% else %}
                            Your cart is empty.
                        {% endif %}
                    {% endwith %}
                </div>
            </div>
        </div>
    </header>

以便只要购物车添加商品后，每个页面的购物车中商品信息的一致性。

                    第八章 订单管理

当购物车要支付的时候，就应该将订单保存在数据库里。订单包含顾客信息和他们购买的商品信息。
为了方便订单管理，我们创建一个独立的应用orders。

一、 创建订单应用
1. 在pycharm的Terminal中输入下面的指令来创建新的应用：
    (webvenv) F:\www\shopshow>python manage.py startapp orders

2. 将应用添加到项目settings.py的INSTALLED_APPS
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'shop',
        'pure_pagination',
        'cart',
        'orders',
    ]

二、创建订单应用的数据模型：

我们需要一个模型来保存订单信息，另外一个模型用来保存购买的商品，包括价格和数量。
1. 打开orders应用下的models.py, 添加如下模型的代码：

from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


2. 迁移生成数据库表单，在Terminal中输入如下命令：

    (webvenv) F:\www\shopshow>python manage.py makemigrations orders
    (webvenv) F:\www\shopshow>python manage.py migrate orders

三、将订单模型注册到后天管理网站

编辑orders应用下的admin.py文件，添加如下代码：

from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

四、创建用户订单
   当用户希望产生一个订单的时候，我们需要刚刚创建的订单模型用来保存购物车中的数据。创建一个新的订单大致需要如下
步骤：
    1. 为用户提供一个窗体用来填写相关数据。
    2. 根据用户输入的数据创建一个订单实例， 然后为购物车中的每件产品创建一个相应的订单项目实例。
    3. 清空购物车，并且跳转用户到一个成功页面。

4.1 创建一个订单窗体，方便收集用户信息，在orders应用中，添加forms.py，输入如下代码：

from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']

4.2 创建一个处理订单的视图，在views.py中添加如下代码：

from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # 清空购物车
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

4.3 创建订单页面
在create.html页面中，因为使用django自己渲染form域，以便能够使用bootstrap中form的样式，需要自定义个
模板过滤器。
1. 在orders应用中，添加templatetags包，并在其中创建custom_css.py文件，输入如下代码：
from django import template

register = template.Library()


@register.filter(name='addclass')
def addclass(field, given_class):
    existing_classes = field.field.widget.attrs.get('class', None)
    if existing_classes:
        if existing_classes.find(given_class) == -1:
            # if the given class doesn't exist in the existing classes
            classes = existing_classes + ' ' + given_class
        else:
            classes = existing_classes
    else:
        classes = given_class
    return field.as_widget(attrs={"class": classes})

2. 在create.html页面中使用时，首先要引入该模板过滤器
{% extends 'shop/base-4.1.1.html' %}
{% load custom_css %}
{% load static %}
...
3. 为了在form中输入控件都呈现bootstrap定义的css
...
                <form action="." method="post">
                    {% for field in form %}
                        <div class="form-group fieldWrapper">
                            {{ field.errors }}
                            {{ field.label_tag }}
                            {{ field|addclass:"form-control form-control-sm" }}
                            {% if field.help_text %}
                            <p class="help">{{ field.help_text|safe }}</p>
                            {% endif %}
                        </div>
                    {% endfor %}

                    <div><input type="submit" class="btn btn-primary btn-block" value="Place order"> </div>
                    {% csrf_token %}
                </form>
...


4.4 安装celery实现异步任务

在视图中执行的任何任务都会需要时间，从而影响对应用请求的响应。但是有些任务可能无法立即返回，
这样就给用户很不好的使用体验，比如发送邮件就是这样的问题。解决这类问题的有效方法就是使用异步任务
处理。
Celery不仅能够创建异步任务，让他们尽快执行，也可以按计划在指定时间执行。我们的项目中，涉及在用户
完成一个订单后，向其发送一封电子邮件。

1. 安装Celery
    pip install celery

Celery需要一个消息broker，RabbitMQ就是一个能与Celery很好集成的broker

2. 安装RabbitMQ
windows下访问 https://www.rabbitmq.com/download.html下载安装程序，进行安装。
安装完成后，启动RabbitMQ server

3. 把Celery添加到shopshow。在shopshow下新建celery.py文件，添加如下代码：

import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopshow.settings')

app = Celery('shopshow')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

4. 为了确保django启动是装载celery模块，需要在shopshow内的__init__.py中添加如下代码

    from .celery import app as celery_app

完成了上述设置，就可以开始异步任务了。

5. 在应用orders中添加异步任务。首先在orders应用中添加tasks.py模块，这里是celery
寻找异步任务的地方。添加如下代码：

from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    '''当一个订单成功创建后，
    发送一个email通知'''
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order. Your order id is {}.'.format(order.first_name,
                                                                                               order.id)
    mail_sent =send_mail(subject, message,
                         'hflag@163.com',
                         [order.email])
    return mail_sent

上述代码就是发送邮件，为了简化邮件发送，这里在项目settings.py中添加如下的邮件backend
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

6. 在相应的视图中使用异步任务，找到order_create视图，修改代码如下：

from cart.cart import Cart
from .tasks import order_created


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # 清空购物车
            cart.clear()

            # 开始异步任务
            order_created.delay(order.id)

            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

7. 测试异步任务
在cmd终端中进入项目所在环境（所使用的虚拟环境），输入如下命令：
    celery -A shopshow worker --pool=solo -l info

这样celery worker就已经运行并准备好处理任务。

接下来启动项目服务器，向购物车添加一些商品，完成订单，在上面的cmd终端中查看异步任务的完成情况。

                    第九章 管理支付和订单

一、集成支付网关

支付网关可以处理在线支付。使用支付网关，可以管理客户订单，安全、可靠的完成第三方支付。目前有很多
支付网关可以选择，我们选择PayPal是因为它是目前最流行的支付网关。

PayPal提供了几种方法在网站中集成。标准的集成包括一个‘Buy now’按钮，或许你在其他网站中已经见到过。
我们计划集成PayPal支付，同样包括‘Buy now’在我们的网站。

PayPal将处理支付，并且发送一个通知到我们的网站用来表明支付状态。

1. 准备工作
  进入PayPal官网，申请账户，注意一定要选择‘Bussiness Account'。

2. 安装 django-paypal
  在Terminal中，通过下面指令，安装PayPal：
   pip install django-paypal

3. 配置PayPal， 在shopshow的settings.py中，添加该应用
    INSTALLED_APPS = [
    # ...
    'paypal.standard.ipn',
    ]

   同时，添加如下代码：
   # django-paypal settings
    PAYPAL_RECEIVER_EMAIL = '532843488@qq.com'
    PAYPAL_TEST = True

4. 迁移数据库。在Terminal中输入下列命令：
    python manage.py migrate

5. 添加PayPal的URLs。在项目shopshow在urls.py中添加如下代码：
    path('payment/', include('payment.urls', namespace='payment')),

二、创建一个新的应用’payment'，用来管理支付过程

1. 创建应用payment
    python manage.py startapp payment

2. 编辑settings.py， 添加应用到配置文件
    INSTALLED_APPS = [
    # ...
    'paypal.standard.ipn',
    'payment',
    ]

3. 修改orders应用中的views.py，添加下面的代码：

from django.shortcuts import render, redirect
from django.urls import reverse

def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            ...
            # 清空购物车
            cart.clear()

            # 开始异步任务
            order_created.delay(order.id)

            # set the order in th session
            request.session['order_id'] = order.id

            # redirect to the payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})

4. 编辑payment应用中的views.py文件，添加如下代码：

from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order


def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % order.get_total_cost().quantize(Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host,reverse('payment:canceled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html',
                  {'order': order, 'form': form})


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')

5. 编辑payment应用中的urls.py

from django.urls import path
from . import views


app_name = 'payment'
urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('done/', views.payment_done, name='done'),
    path('canceled/', views.payment_canceled, name='canceled'),
]
同时不要忘记了将payment应用到urls.py添加到项目的urls.py里。

6. 编写payment显示页面， 在payment应用下新建templates/payment.并且添加
process.html, done.html, canceled.html

它们的代码如下：

（1）process.html

{% extends 'shop/base-4.1.1.html' %}
{% load custom_css %}
{% load static %}
<link href="{% static 'css/style.css' %}" rel="stylesheet">

{% block title %}
    Pay using PayPal
{% endblock %}

{% block content %}
   ...
    <div class="container">
        <div class="row ">
            <div class="col-12 ">
                <h1>Pay using PayPal</h1>
                {{ form.render }}
            </div>
        </div>

    </div>
{% endblock %}

(2) done.html

{% extends 'shop/base-4.1.1.html' %}
{% load custom_css %}
{% load static %}
<link href="{% static 'css/style.css' %}" rel="stylesheet">

{% block title %}
    Pay using PayPal
{% endblock %}

{% block content %}
   ...
    <div class="container">
        <div class="row ">
            <div class="col-12 ">
                <h1>Your payment was successful</h1>
                <p>Your payment has been successfully received.</p>
            </div>
        </div>

    </div>
{% endblock %}

(3) canceled.html

{% extends 'shop/base-4.1.1.html' %}
{% load custom_css %}
{% load static %}
<link href="{% static 'css/style.css' %}" rel="stylesheet">

{% block title %}
    Pay using PayPal
{% endblock %}

{% block content %}
   ...
    <div class="container">
        <div class="row ">
            <div class="col-12 ">
                <h1>Your payment has not been processed</h1>
                <p>There was a problem processing your payment.</p>
            </div>
        </div>

    </div>
{% endblock %}

三、使用PayPal沙箱

1. PayPal沙箱个人账户设置
 打开http://developer.paypal.com，使用PayPal商务账号登录。 点击‘Dashboard'菜单项，就可以看到
 Sandbox下的Accounts。
 找到个人账户，修改密码后，用于后面的购买测试。

2. 启动服务器，浏览商品，并添加进入购物车后，checkout，体会PayPal支付过程。

3. 测试支付的时候，是一定要有两个PayPal账号才可以的！！

##



