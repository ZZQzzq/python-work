# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from operation.models import UserFavorite, UserBook, BookComments
from .models import BookKind, Book, BookTag, BookDetail
from .forms import UserAskForm

# Create your views here.
#  图书列表功能
class BookView(View):
    def get(self, request):
        # 所有图书
        all_books = Book.objects.all()
        # 取点击量排名前三的热门图书
        hot_books = all_books.order_by("-click_nums")[:3]

        # 取出tag筛选结果
        booktag = request.GET.get('booktag', "")
        if booktag:
            all_books = all_books.filter(book_tag=booktag)  # 因为city是外键，在数据库中保存为city_id
        # 取出类别筛选结果
        bookkind_id = request.GET.get('bookkind', "")
        if bookkind_id:
            all_books = all_books.filter(book_kind_id=int(bookkind_id))  # 因为bookKind是外键，在数据库中保存为bookkind_id

        book_nums = all_books.count()

        # 全局搜索功能
        search_keywords = request.GET.get('keywords', "")
        print search_keywords
        if search_keywords:
            # 相当于like语句 i表示不区分大小写
            all_books = all_books.filter(Q(book_name__icontains=search_keywords)|Q(book_kind__book_name__icontains=search_keywords)|Q(book_info__icontains=search_keywords))

        # 排序功能
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "click_nums":  # 根据学生人数排序
                all_books = all_books.order_by("-click_nums")  # order_by("-click_nums")表示倒序排列
            elif sort == "fav_nums":
                all_books = all_books.order_by("-fav_nums")
            elif sort == 'stars':
                all_books = all_books.order_by("-stars")

        # 对图书列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
        p = Paginator(all_books, 50)
        books = p.page(page)

        # 所有类型
        all_kinds = BookKind.objects.all()

        # 根据不同的大标签，显示其下小标签.当选择全部的时候，tag_id就为0
        tag_id = 0
        if booktag == 'wx': tag_id = 1
        elif booktag == "wh": tag_id = 2
        elif booktag == "sh": tag_id = 3
        elif booktag == "kj": tag_id = 4
        elif booktag == "jg": tag_id = 5
        elif booktag == "lx": tag_id = 6

        alltag = BookTag.objects.all()
        tag = alltag.filter(id=tag_id)  # 取出大标签，是一个列表数组，实际上只有一个值，取tag[0]即可
        # 需要注意的是，tag_id如果为0的话，此时tag取出来是一个空列表，所以需要进行判断，否则会出现列表索引超出范围的错误
        if tag:
            tag = tag[0]


        return render(request, "book-list.html", {
            "all_books": books,
            "all_kinds": all_kinds,
            "book_nums": book_nums,
            "bookkind_id": bookkind_id,
            "book_tag": booktag,
            "hot_books": hot_books,
            "sort": sort,
            "tag": tag,
            "tag_id": tag_id
        })
# class AddUserAskView(View):
#     # 用户添加查询
#     def post(self,request):
#         userask_form = UserAskForm(request.POST)
#         if userask_form.is_valid():  # 表单验证成功
#             book_name = request.POST.get("book_name", "")
#             book_type = request.POST.get("book_type", "")
#             book_star = request.POST.get("book_star", 0)
#             if book_name:
#                 book = Book.objects.filter(book_name=book_name)
#             elif book_type:
#                 book = Book.objects.filter(book_tag=book_type)
#             elif book_star:
#                 book = Book.objects.filter(book_tag=book_type)
#
#
#
#         return render(request, "book_detail.html", {"book": book})
"""
class BookHomeView(View):
    def get(self, request, book_id):
        current_page = "home"
        book = BookDetail.objects.get(id=int(book_id))
        #  保存到UserFavorite这张表中
        # has_fav = False
        # if request.user.is_authenticated():
        #     if UserFavorite.objects.filter(user=request.user, fav_id=book.id, fav_type='sj'):
        #         has_fav = True
        #  保存到UserBook这张表中
        has_fav = False
        if request.user.is_authenticated():
            if UserBook.objects.filter(user=request.user, book_id=book.id):
                has_fav = True

        return render(request, 'book_detail_homepage.html',
                      {
                          "book": book,
                          "current_page": current_page,
                          "has_fav": has_fav
                      })
class BookDescView(View):
    def get(self, request, book_id):
        current_page = "desc"
        book = BookDetail.objects.get(id=int(book_id))
        # has_fav = False
        # if request.user.is_authenticated():
        #     if UserFavorite.objects.filter(user=request.user, fav_id=book.id, fav_type="sj"):
        #         has_fav = True

        has_fav = False
        if request.user.is_authenticated():
            if UserBook.objects.filter(user=request.user, book_id=book.id):
                has_fav = True

        return render(request, 'book_detail_desc.html',
                      {
                          "book": book,
                          "current_page": current_page,
                          "has_fav": has_fav
                      })
"""
# 图书详情页
class BookDetailView(View):
    def get(self, request, book_no):   # 必须将url中传进来的book_no传进来
        book = BookDetail.objects.get(book_no=book_no)
        # 触发该事件后，应该将图书点击数加一
        book.click_nums += 1  # book_detail表
        book.save()
        # 点击率最高的图书显示：
        all_books = Book.objects.all()
        hot_books = all_books.order_by("-click_nums")[:1]
        hot_book = hot_books[0]
        # 相关图书推荐，根据tag标签是否相关来推荐，可能为空
        book1 = Book.objects.get(book_no=book_no)
        # 触发该事件后，应该将图书点击数加一
        book1.click_nums += 1  # book表
        book1.save()
        # 标签
        real_tag = ""
        book1_tag = book1.book_tag
        if book1_tag == "wx": real_tag= "文学"
        if book1_tag == "wh": real_tag = "文化"
        if book1_tag == "kj": real_tag = "科技"
        if book1_tag == "jg": real_tag = "经管"
        if book1_tag == "sh": real_tag = "生活"
        if book1_tag == "lx": real_tag = "流行"
        tag = book1.book_kind_id
        if tag:
            relate_books = Book.objects.filter(book_kind=tag)[:5]  # 只传一个
        else:
            relate_books = []

        # 推荐图书集合
        recommendations = book.recommendations.split(',')
        # 目录整理
        mulu = book.mu_lu.split('|')

        # 判断是否收藏
        book_has_fav = False  # 左边的收藏
        hot_has_fav = False  # 右边的收藏
        if request.user.is_authenticated():
            if UserBook.objects.filter(user=request.user, book_id=book1.id):
                book_has_fav = True
            if UserBook.objects.filter(user=request.user, book_id=hot_book.id):
                hot_has_fav = True

        return render(request, "new_book_detail.html",
        {
            "book": book,
            "book1": book1,
            "relate_books": relate_books,
            "book_has_fav": book_has_fav,
            "real_tag": real_tag,
            "hot_book": hot_book,
            "hot_has_fav": hot_has_fav,
            "recommendations":recommendations,
            "mulu":mulu
        })
# 用户评论
class BookCommentView(View):
    def get(self, request, book_no):
        book1 = Book.objects.get(book_no=book_no)
        book2 = BookDetail.objects.get(book_no=book_no)
        book_id = book1.id
        all_comments = BookComments.objects.all().filter(book_id=book_id).order_by("-likenum")

        # 相关图书推荐，根据用户收藏表内容来判断是否相关来推荐，可能为空
        id = Book.objects.get(book_no=book_no).id
        users = UserBook.objects.filter(book_id=id)  # 找出收藏该图书的记录
        relate_books = [] # 取十本图书进行显示
        for user in users:
            user_books = UserBook.objects.filter(user_id=user.user_id)  # 找出这些用户收藏的电影
            for user_book in user_books:  # 将这些图书加入推荐目录
                relate_book = Book.objects.get(id=user_book.book_id)
                print (relate_book.book_name)
                relate_books.append(relate_book)
        relate_books = set(relate_books[:10]) # 使用set()去重


        return render(request, "new_book_comment.html", {
            "book1": book1,
            "book2": book2,
            "all_comments": all_comments,
            "relate_books": relate_books
        })

# 用户添加图书评论
class AddBookCommentView(View):
        def post(self, request):
            if not request.user.is_authenticated():
                return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
            book_no = request.POST.get('book_no', 0)
            comments = request.POST.get('comments', 0)
            if book_no and comments:
                book_comments = BookComments()
                book = Book.objects.get(book_no=book_no)
                book_comments.book = book
                book_comments.comments = comments
                book_comments.user = request.user
                book_comments.save()
                return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":" 添加失败"}', content_type='application/json')

# 更新likenum
class LikenumView(View):
    def post(self, request):
            print ("点赞数加一")
            book_id = request.POST.get('book_id', 0)
            user_id = request.POST.get('user_id', 0)
            comment_id = request.POST.get('comment_id', 0)
            bookcomment = BookComments.objects.get(user_id=int(user_id), book_id=int(book_id), id=int(comment_id))
            bookcomment.likenum += 1
            bookcomment.save()
            return HttpResponse('{}', content_type='application/json')

# 更新dislikenum
class DislikenumView(View):
     def post(self, request):
        print ("点踩数加一")
        book_id = request.POST.get('book_id', 0)
        user_id = request.POST.get('user_id', 0)
        comment_id = request.POST.get('comment_id', 0)
        bookcomment = BookComments.objects.get(user_id=int(user_id), book_id=int(book_id), id=int(comment_id))
        bookcomment.dislikenum += 1
        bookcomment.save()
        return HttpResponse('{}', content_type='application/json')

# 收藏与取消收藏功能
class AddFavView(View):
    # 保存到UserFavorite这张表中
    # def post(self, request):
    #     fav_id = request.POST.get('fav_id', 0)
    #     print fav_id
    #     fav_type = request.POST.get('fav_type', "")
    #     print fav_type
    #     # 在用户未登录的情况下，python django内置的一个user类，通过is_authenticated()方法来判断是否 处于登陆状态
    #     if not request.user.is_authenticated():
    #         return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
    #         # AJAX来控制跳转到登陆界面
    #     exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=fav_type)
    #     #exist_record = UserBook.objects.filter(user=request.user, fav_id=int(fav_id))
    #     if exist_record:
    #         # 记录已经存在，则表示用户想要取消收藏
    #         exist_record.delete()
    #         return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
    #     else:
    #         user_fav = UserFavorite()
    #         #user_fav = UserBook()
    #         # 若fav_id为0，说明并没有点击收藏
    #         if int(fav_id) > 0 and fav_type:
    #             user_fav.user = request.user
    #             user_fav.fav_id = int(fav_id)
    #             user_fav.fav_type = fav_type
    #            # user_fav.book_id = int(fav_id)
    #             user_fav.save()
    #             return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
    #         else:
    #             return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')
    #  保存到UserBook这张表中
    def post(self, request):
        fav_no = request.POST.get('fav_no', "")
        fav_id = Book.objects.get(book_no=fav_no).id
        fav_type = request.POST.get('fav_type', "")
        print fav_id
        print fav_type
        book = Book.objects.get(book_no=fav_no)
        bookdetail = BookDetail.objects.get(book_no=fav_no)
        # 在用户未登录的情况下，python django内置的一个user类，通过is_authenticated()方法来判断是否处于登陆状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
            # AJAX来控制跳转到登陆界面

        exist_record = UserBook.objects.filter(user=request.user, book_id=int(fav_id))
        print (exist_record)
        if exist_record:
            # 记录已经存在，则表示用户想要取消收藏
            # 收藏数减一
            book.fav_nums -= 1
            book.save()
            bookdetail.fav_nums -= 1
            bookdetail.save()
            exist_record.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserBook()
            # 若fav_id为0，说明并没有点击收藏
            if int(fav_id) > 0 and fav_type:
                user_fav.user = request.user
                user_fav.book_id = int(fav_id)
                user_fav.save()
                print("收藏")
                # 收藏数加一
                book.fav_nums += 1
                book.save()
                bookdetail.fav_nums += 1
                bookdetail.save()
                return HttpResponse('{"status":"success", "msg":"-0-已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')





