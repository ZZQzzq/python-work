# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/17 23:41'

import xadmin
from models import BookKind, Book, BookDetail, BookTag

class BookTagAdmin(object):
    list_display = ['book_name', 'add_time']
    search_fields = ['book_name', 'add_time']   # 查询
    list_filter = ['book_name', 'add_time']   # 通过时间筛选
xadmin.site.register(BookTag, BookTagAdmin)


class BookKindAdmin(object):
    list_display = ['book_name', 'book_tag', 'add_time']
    search_fields = ['book_name', 'book_tag', 'add_time']   # 查询
    list_filter = ['book_name', 'book_tag', 'add_time']   # 通过时间筛选
xadmin.site.register(BookKind, BookKindAdmin)

class BookAdmin(object):
    list_display = ['book_name', 'book_no', 'book_info', 'book_url', 'book_tag', 'book_kind', 'stars', 'click_nums', 'fav_nums', 'image', 'add_time']
    search_fields = ['book_name', 'book_no', 'book_info', 'book_url', 'book_tag', 'book_kind', 'stars', 'click_nums', 'fav_nums', 'image', 'add_time']   # 查询
    list_filter = ['book_name', 'book_no', 'book_info', 'book_url', 'book_tag', 'book_kind', 'stars', 'click_nums', 'fav_nums', 'image', 'add_time']   # 通过时间筛选
xadmin.site.register(Book, BookAdmin)

class BookDetailAdmin(object):
    list_display = ['book_no', 'book_name', 'book_author', 'book_public', 'book_year', 'book_page', 'book_price', 'votenum', 'stars',
                    'book_intro', 'author_intro', 'book_others', 'mu_lu', 'recommendations', 'comments', 'click_nums', 'fav_nums', 'add_time']
    search_fields = ['book_no', 'book_name', 'book_author', 'book_public', 'book_year', 'book_page', 'book_price', 'votenum', 'stars',
                     'book_intro', 'author_intro', 'book_others', 'mu_lu', 'recommendations', 'comments', 'click_nums', 'fav_nums', 'add_time']   # 查询
    list_filter = ['book_no', 'book_name', 'book_author', 'book_public', 'book_year', 'book_page', 'book_price', 'votenum', 'stars',
                   'book_intro', 'author_intro', 'book_others', 'mu_lu', 'recommendations', 'comments', 'click_nums', 'fav_nums', 'add_time'] # 通过时间筛选
xadmin.site.register(BookDetail, BookDetailAdmin)
