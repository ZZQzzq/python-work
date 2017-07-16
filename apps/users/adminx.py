# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/17 23:26'

import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner, UserProfile
from xadmin.plugins.auth import UserAdmin

# # 将用户权限中系统自带的的用户信息卸载掉
# from django.contrib.auth.models import User
# xadmin.site.unregister(User)
# # 注册用户信息
# class UserProfileAdmin(UserAdmin):
#     pass
# xadmin.site.register(UserProfile, UserProfileAdmin)
# 全站配置
class BaseSetting(object):
    enable_themes = True   #开启主题功能
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)

# logo全站设置
class GlobalSetting(object):
    site_title = "爬虫后台管理系统"  # 左上角
    site_footer = "爬虫在线网"  # 底部
    menu_style = "accordion"  # 将APP收起来，使页面简洁

xadmin.site.register(views.CommAdminView, GlobalSetting)


# 注册 EmailVerifyRecord 这张表
class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type', 'send_time']  # 查询
    list_filter = ['code', 'email', 'send_type', 'send_time']  # 通过时间筛选
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

# 注册 Banner 这张表
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index', 'add_time']  # 查询
    list_filter = ['title', 'image', 'url', 'index', 'add_time']  # 通过时间筛选
xadmin.site.register(Banner, BannerAdmin)