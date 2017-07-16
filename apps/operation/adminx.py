# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/20 21:36'

import xadmin
from models import UserFavorite, UserBook, UserMessage, UserMovie, BookComments, MovieComments


class BookCommentsAdmin(object):
    list_display = ['user', 'book', 'comments', 'add_time']
    search_fields = ['user', 'book', 'comments', 'add_time']  # 查询
    list_filter = ['user', 'book', 'comments', 'add_time']  # 通过时间筛选
xadmin.site.register(BookComments, BookCommentsAdmin)

class MovieCommentsAdmin(object):
    list_display = ['user', 'movie', 'comments', 'add_time']
    search_fields = ['user', 'movie', 'comments', 'add_time']  # 查询
    list_filter = ['user', 'movie', 'comments', 'add_time']  # 通过时间筛选
xadmin.site.register(MovieComments, MovieCommentsAdmin)


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type', 'add_time']  # 查询
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']  # 通过时间筛选
xadmin.site.register(UserFavorite, UserFavoriteAdmin)

class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read', 'add_time']  # 查询
    list_filter = ['user', 'message', 'has_read', 'add_time']  # 通过时间筛选
xadmin.site.register(UserMessage, UserMessageAdmin)

class UserBookAdmin(object):
    list_display = ['user', 'book', 'add_time']
    search_fields = ['user', 'book', 'add_time']  # 查询
    list_filter = ['user', 'book', 'add_time']  # 通过时间筛选
xadmin.site.register(UserBook, UserBookAdmin)

class UserMovieAdmin(object):
    list_display = ['user', 'movie', 'add_time']
    search_fields = ['user', 'movie', 'add_time']  # 查询
    list_filter = ['user', 'movie', 'add_time']  # 通过时间筛选
xadmin.site.register(UserMovie, UserMovieAdmin)


