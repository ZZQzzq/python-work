# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
# 在默认生成的user表基础上新增一些字段
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u"昵称", default="")
    birthday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=7, choices=(("male", u"男"), ("female", u"女")), default="female", verbose_name=u"性别")
    address = models.CharField(max_length=100, default=u"",verbose_name=u"住址")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u"联系方式")
    image = models.ImageField(upload_to="image/%Y/%m", default=u"image/default.png", max_length=100,  verbose_name=u"头像")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
    # 重载__unicode__函数
    def __unicode__(self):
        return self.username

    def unread_nums(self):
        # 获取用户未读信息数量
        # import必须放在这里，否则会与operation的import循环调用
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(choices=(("register", u"注册"), ("forget", u"找回密码"), ("update_email", u"修改邮箱")), verbose_name=u"发送方式", max_length=13)
    send_time = models.DateField(default=datetime.now, verbose_name=u"发送时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name
    # 重载unicode方法，自定义显示方式
    def __unicode__(self):
        return '{0}（{1}）'.format(self.code, self.email)
class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name=u"轮播图", max_length=100)
    url = models.URLField(max_length=200, verbose_name=u"访问地址")  # 轮播图片地址
    index = models.IntegerField(default=100, verbose_name=u"顺序")  # 播放顺序
    add_time = models.DateField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name
