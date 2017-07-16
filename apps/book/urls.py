# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/18 13:07'


from django.conf.urls import url, include
from .views import BookView, AddFavView, BookDetailView, BookCommentView, AddBookCommentView, LikenumView, DislikenumView

urlpatterns = [
    url(r'^book_list/$', BookView.as_view(), name="book_list"),
    # url(r'^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    # 图书详情页
    url(r'^detail/(?P<book_no>\d+)/$', BookDetailView.as_view(), name="book_detail"),
    # 图书评论
    url(r'^comment/(?P<book_no>\d+)/$', BookCommentView.as_view(), name="book_comment"),
    # 图书收藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add_fav"),
    # 添加图书评论
    url(r'^add_comment/$', AddBookCommentView.as_view(), name="add_comment"),
    # 点赞人数更新
    url(r'^like_num/$', LikenumView.as_view(), name="like_num"),
    # 踩的人数更新
    url(r'^dislike_num/$', DislikenumView.as_view(), name="dislike_num"),


]