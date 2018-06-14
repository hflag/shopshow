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