# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from django.db import models
from datetime import datetime

from users.models import UserProfile
from book.models import Book
from movies.models import Movie
# Create your models here.
class BookComments(models.Model):
    "图书评论"
    user = models.ForeignKey(UserProfile, verbose_name=u"用户名")
    book = models.ForeignKey(Book, verbose_name=u"图书")
    comments = models.CharField(max_length=200, verbose_name=U"评论")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    likenum = models.IntegerField(default=0,verbose_name="点赞次数")
    dislikenum = models.IntegerField(default=0,verbose_name="被踩次数")
    class Meta:
        verbose_name = u"图书评论"
        verbose_name_plural = verbose_name

class MovieComments(models.Model):
    "电影评论"
    user = models.ForeignKey(UserProfile, verbose_name=u"用户名")
    movie = models.ForeignKey(Movie, verbose_name=u"电影")
    comments = models.CharField(max_length=200, verbose_name=U"评论")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    likenum = models.IntegerField(default=0, verbose_name="点赞次数")
    dislikenum = models.IntegerField(default=0, verbose_name="被踩次数")
    class Meta:
        verbose_name = u"电影评论"
        verbose_name_plural = verbose_name

class UserFavorite(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户名")
    fav_id = models.IntegerField(default=0, verbose_name=u"数据ID")
    fav_type = models.CharField(max_length=5, choices=(("sj", "书籍"), ("dy", "电影")),default="sj", verbose_name=u"收藏类型")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"用户收藏"
        verbose_name_plural = verbose_name

class UserMessage(models.Model):
    # 区分是针对某个用户的消息还是发给全员的消息
    user = models.IntegerField(default=0, verbose_name=u"接收用户")
    message = models.CharField(max_length=500, verbose_name=u"消息内容")
    # False表示未读，True表示已读
    has_read = models.BooleanField(default=False, verbose_name=u"是否已读")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"用户消息"
        verbose_name_plural = verbose_name

class UserBook(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    book = models.ForeignKey(Book, verbose_name=u"图书")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"用户图书"
        verbose_name_plural = verbose_name

class UserMovie(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户")
    movie = models.ForeignKey(Movie, verbose_name=u"电影")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"用户电影"
        verbose_name_plural = verbose_name
