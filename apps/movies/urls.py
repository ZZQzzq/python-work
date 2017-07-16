# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/23 11:12'

from django.conf.urls import url, include
from .views import MovieView, MovieDetailView, MovieCommentView, AddMovieCommentView, AddFavView, LikenumView, DislikenumView

urlpatterns = [
    url(r'^movie_list/$', MovieView.as_view(), name="movie_list"),
    # url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    # 图书详情页
    url(r'^detail/(?P<movie_no>\d+)/$', MovieDetailView.as_view(), name="movie_detail"),
    # 图书评论
    url(r'^comment/(?P<movie_no>\d+)/$', MovieCommentView.as_view(), name="movie_comment"),
    # 电影收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),
    # 添加电影评论
    url(r'^add_comment/$', AddMovieCommentView.as_view(), name="add_comment"),
    # 点赞人数更新
    url(r'^like_num/$', LikenumView.as_view(), name="like_num"),
    # 踩的人数更新
    url(r'^dislike_num/$', DislikenumView.as_view(), name="dislike_num"),
]