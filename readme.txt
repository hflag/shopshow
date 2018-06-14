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
