# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime
from django.db import models

# Create your models here.
# 大类【经管，科技，文学，文化，流行，生活】
class BookTag(models.Model):
    book_name = models.CharField(max_length=20, verbose_name=u"图书大类")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"图书总类别"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.book_name
# 小类
class BookKind(models.Model):
    book_name = models.CharField(max_length=20, verbose_name=u"图书小类")
    book_tag = models.ForeignKey(BookTag, verbose_name=u"大类别", null=True, blank=True)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"图书具体类别"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.book_name

class Book(models.Model):
    book_name = models.CharField(max_length=50, verbose_name=U"图书名")
    book_no = models.CharField(max_length=50, verbose_name=U"图书编号")
    book_info = models.TextField(verbose_name=U"图书详情")
    book_url = models.URLField(max_length=500, verbose_name=u"图书链接")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    book_tag = models.CharField(default="wx", verbose_name=u"图书标签", max_length=10,choices=(("wx", "文学"),("wh", "文化"), ("kj","科技"), ("jg","经管"), ("lx","流行"), ("sh", "生活")))
    book_kind = models.ForeignKey(BookKind, verbose_name=u"图书类型")
    stars = models.FloatField(max_length=10, verbose_name=u"评分")
    click_nums = models.IntegerField(default=0, verbose_name=U"浏览人数")
    fav_nums = models.IntegerField(default=0, verbose_name=U"收藏人数")
    image = models.ImageField(upload_to="book/%Y/%m", verbose_name=u"封面图", max_length=100)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"图书"
        verbose_name_plural = verbose_name
    # 重载unicode方法
    def __unicode__(self):
        return self.book_name
    # 获取收藏了该图书的用户(五个)
    def get_fav_users(self):
        return self.userbook_set.all()[:5]

class BookDetail(models.Model):
    book_no = models.CharField(max_length=50, verbose_name=u"图书编号")
    book_name = models.CharField(max_length=100, verbose_name=u"书名")
    book_author = models.CharField(max_length=100, verbose_name=u"作者")
    book_public = models.CharField(max_length=100, verbose_name=u"出版社")
    book_year = models.CharField(max_length=20, verbose_name=u"出版时间")
    book_page = models.IntegerField(default=0, verbose_name=u"页数")
    book_price = models.CharField(max_length=30, verbose_name=u"价格")
    votenum = models.IntegerField(default=0, verbose_name=u"评论人数")
    stars = models.FloatField(max_length=10, verbose_name=u"评分")
    book_intro = models.TextField(verbose_name=u"图书简介")
    author_intro = models.TextField(verbose_name=u"作者简介")
    book_others = models.TextField(verbose_name=u"丛书信息")
    mu_lu = models.TextField(verbose_name=u"目录")
    recommendations = models.CharField(max_length=250,verbose_name=u"相关推荐")
    comments = models.TextField(verbose_name=u"评论")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    image = models.ImageField(upload_to="book_detail/%Y/%m", default="", verbose_name=u"大图", max_length=100)
    book_info = models.TextField(default="", verbose_name=u"图书信息")
    class Meta:
        verbose_name = u"图书详情"
        verbose_name_plural = verbose_name
    # 重载unicode方法
    def __unicode__(self):
        return self.book_name



