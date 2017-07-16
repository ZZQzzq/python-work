# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/17 23:27'

import xadmin
from .models import Movie, MovieKind, MovieTag, MovieDetail

class MovieKindAdmin(object):
    list_display = ['movie_name', 'movie_no', 'movie_kind', 'add_time']
    search_fields = ['movie_name', 'movie_no', 'movie_kind', 'add_time']   # 查询
    list_filter = ['movie_name', 'movie_no', 'movie_kind', 'add_time']   # 通过时间筛选
xadmin.site.register(MovieKind, MovieKindAdmin)

class MovieAdmin(object):
    list_display = ['movie_name', 'movie_no', 'movie_info', 'movie_url', 'movie_year', 'stars', 'click_nums', 'fav_nums', 'image', 'add_time']
    search_fields =['movie_name', 'movie_no', 'movie_info', 'movie_url', 'movie_year', 'stars', 'click_nums', 'fav_nums', 'image', 'add_time']   # 查询
    list_filter = ['movie_name', 'movie_no', 'movie_info', 'movie_url', 'movie_year', 'stars', 'click_nums', 'fav_nums', 'image', 'add_time']  # 通过时间筛选
xadmin.site.register(Movie, MovieAdmin)

class MovieTagAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc', 'add_time']  # 查询
    list_filter = ['name', 'desc', 'add_time']  # 通过时间筛选
xadmin.site.register(MovieTag, MovieTagAdmin)

class MovieDetailAdmin(object):
    list_display = ['movie_no', 'movie_name', 'movie_year',  'movie_director', 'movie_pl', 'movie_actor', 'movie_type', 'country',
                    'language', 'movie_ReleaseDate', 'runtime', 'votenum', 'stars', 'movie_intro', 'recommendations', 'comments', 'click_nums',
                    'fav_nums', 'add_time']
    search_fields = ['movie_no', 'movie_name', 'movie_year', 'movie_director', 'movie_pl', 'movie_actor', 'movie_type', 'country',
                    'language', 'movie_ReleaseDate', 'runtime', 'votenum', 'stars', 'movie_intro', 'recommendations', 'comments', 'click_nums',
                    'fav_nums', 'add_time']   # 查询
    list_filter = ['movie_no', 'movie_name', 'movie_year', 'movie_director', 'movie_pl', 'movie_actor', 'movie_type', 'country',
                    'language', 'movie_ReleaseDate', 'runtime', 'votenum', 'stars', 'movie_intro', 'recommendations', 'comments', 'click_nums',
                    'fav_nums', 'add_time']  # 通过时间筛选
xadmin.site.register(MovieDetail, MovieDetailAdmin)