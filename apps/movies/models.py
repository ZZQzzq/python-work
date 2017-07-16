# _*_ coding:utf-8 _*_
from __future__ import unicode_literals

from datetime import datetime
from django.db import models

# Create your models here.
class MovieKind(models.Model):
    movie_name = models.CharField(max_length=50, verbose_name=U"电影名")
    movie_no = models.CharField(max_length=50, verbose_name=u"电影编号")
    movie_kind = models.IntegerField(default=1988, verbose_name=u"上映年份")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"电影类别"
        verbose_name_plural = verbose_name

    # 重载unicode方法
    def __unicode__(self):
        return self.movie_name

class MovieTag(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"类别名称")
    desc = models.CharField(max_length=200, verbose_name=u"类别描述")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"分类"
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class Movie(models.Model):
    movie_name = models.CharField(max_length=100, verbose_name=U"电影名")
    movie_no = models.CharField(max_length=100, verbose_name=U"电影编号")
    movie_info = models.TextField(verbose_name=U"电影详情")
    movie_url = models.CharField(max_length=150, verbose_name=u"电影链接")
    movie_year = models.ForeignKey(MovieTag, default="1988", verbose_name=u"年份")
    stars = models.FloatField(max_length=10, verbose_name=u"评分")
    click_nums = models.IntegerField(default=0, verbose_name=U"浏览人数")
    fav_nums = models.IntegerField(default=0, verbose_name=U"收藏人数")
    image = models.ImageField(upload_to="movie_detail/%Y/%m", verbose_name=u"封面图", max_length=100)
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")

    class Meta:
        verbose_name = u"电影"
        verbose_name_plural = verbose_name
    # 重载unicode方法
    def __unicode__(self):
        return self.movie_name
    # 获取收藏了这部电影的用户(五个)
    def get_fav_users(self):
        return self.usermovie_set.all()[:5]



class MovieDetail(models.Model):
    movie_no = models.CharField(max_length=20, verbose_name=u"电影编号")
    movie_name = models.CharField(max_length=100, verbose_name=u"电影名")
    movie_year = models.CharField(max_length=10, verbose_name=u"电影年份")
    # movie_tag = models.ForeignKey(MovieTag, verbose_name=u"电影类别")
    movie_director = models.CharField(max_length=100, verbose_name=u"电影导演")
    movie_pl = models.CharField(max_length=300, verbose_name=u"电影编剧")
    movie_actor = models.CharField(max_length=800, verbose_name=u"电影主演")
    movie_type = models.CharField(default='无明确类型', max_length=100, verbose_name=u"电影类型")
    country = models.CharField(max_length=100, verbose_name=u"制片国家/地区")
    language = models.CharField(max_length=20, verbose_name=u"语言")
    movie_ReleaseDate = models.CharField(max_length=20, verbose_name=u"上映日期")
    runtime = models.CharField(max_length=10, verbose_name=u"电影时长")
    votenum = models.IntegerField(default=0, verbose_name=u"评论人数")
    stars = models.CharField(max_length=15, verbose_name=u"评分")
    movie_intro = models.TextField(verbose_name=u"电影简介")
    recommendations = models.TextField(verbose_name=u"相关推荐")
    comments = models.TextField(verbose_name=u"评论")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")
    class Meta:
        verbose_name = u"电影详情"
        verbose_name_plural = verbose_name
    # 重载unicode方法
    def __unicode__(self):
        return self.movie_name

