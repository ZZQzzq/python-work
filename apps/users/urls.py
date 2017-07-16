# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__date__ = '2017/4/25 13:41'

from django.conf.urls import url, include
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailView, UpdateEmailView,  MyFavBookView, MyMessageView, MyFavMovieView

urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name="user_info"),
    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),

    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailView.as_view(), name="sendemail_code"),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),

    # 我收藏的的图书
    url(r'^myfav/book/$', MyFavBookView.as_view(), name="myfav_book"),
    # 我收藏的电影
    url(r'^myfav/movie/$', MyFavMovieView.as_view(), name="myfav_movie"),

    # 我的消息
    url(r'^mymessage/$', MyMessageView.as_view(), name="mymessage"),

]

