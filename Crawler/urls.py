# -*- coding:utf-8 -*-
"""Crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve  # 用于处理静态文件
from extra_apps import xadmin
from Crawler.settings import MEDIA_ROOT #, STATIC_ROOT
from django.views.static import serve  # 用于处理静态文件

# 使用类定义登录方式
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView
from users.views import ModifyPwdView, LogoutView,IndexView
from book.views import BookView
from movies.views import MovieView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),  # 验证码图片url

    url(r'^$', IndexView.as_view(), name="index"),  # 首页
    url(r'^login/$', LoginView.as_view(), name="login"),  # 登陆
    url(r'^logout/$', LogoutView.as_view(), name="logout"),  # 登出

    # url(r'^login/$', user_login, name="login"),  # Login千万不能加括弧，因为这里只是一个句柄，指向login函数，而不是调用
    url(r'^register/$', RegisterView.as_view(), name="register"),  # 此处调用的是LoginView的as_view()方法
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),   # 用户激活
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),  # 忘记密码
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),   # 修改密码
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),  # 重置密码

    # 图书列表首页
    url(r'^book_list/$', BookView.as_view(), name="book_list"),
    # 电影列表首页
    url(r'^movie_list/$', MovieView.as_view(), name="movie_list"),

    # 图书模块url分发机制
    url(r'^book/', include('book.urls', namespace="book")),
    # 电影模块url分发机制
    url(r'^movie/', include('movies.urls', namespace="movie")),
    # 用户信息模块url分发机制
    url(r'^users/', include('users.urls', namespace="users")),

    # 配置上传图片文件URL路径的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

]

# 全局404页面配置
handler404 = 'users.views.page_not_found'
# 全局500页面配置
handler500 = 'users.views.page_error'