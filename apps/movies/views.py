# _*_ coding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q

from operation.models import UserFavorite, UserMovie, MovieComments
from .models import Movie, MovieDetail, MovieTag
# from .forms import UserAskForm


# Create your views here.
class MovieView(View):
    # 电影列表功能
    def get(self, request):
        # 所有图书
        all_movies = Movie.objects.all()
        # 取点击量排名前三的热门电影
        hot_movies = all_movies.order_by("-click_nums")[:3]

        # 取出所有的标签
        all_tags = MovieTag.objects.all()

        # 全局搜索功能
        search_keywords = request.GET.get('keywords', "")
        if search_keywords:
            # 相当于like语句 i表示不区分大小写
            all_movies = all_movies.filter(
                Q(movie_name__icontains=search_keywords) | Q(movie_year__name__icontains=search_keywords) | Q(
                    movie_info__icontains=search_keywords))

        # 取出tag筛选结果
        movietag = request.GET.get('movietag', "")
        this_tag = MovieTag.objects.all().filter(name=movietag)
        if movietag:
            all_movies = all_movies.filter(movie_year_id=this_tag[0].id)  # movie_year是外键，在数据库中保存为movietag_id

        movie_nums = all_movies.count()
        # 排序功能
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "click_nums":  # 根据学生人数排序
                all_movies = all_movies.order_by("-click_nums")  # order_by("-click_nums")表示倒序排列
            elif sort == "fav_nums":
                all_movies = all_movies.order_by("-fav_nums")
            elif sort == "stars":
                all_movies = all_movies.order_by("-stars")

        # 对电影列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
        p = Paginator(all_movies, 50)
        movies = p.page(page)

        return render(request, "movie_list.html", {
            "all_movies": movies,
            "all_tags": all_tags,
            "movie_nums": movie_nums,
            "movie_tag": movietag,
            "hot_movies": hot_movies,
            "sort": sort,
        })

# 电影详情页
class MovieDetailView(View):
    def get(self, request, movie_no):   # 必须将url中传进来的movie_no传进来
        movie = MovieDetail.objects.get(movie_no=movie_no)
        # 触发该事件后，应该将图书点击数加一
        movie.click_nums += 1  # movie_detail表
        movie.save()
        movie1 = Movie.objects.get(movie_no=movie_no)
        # 触发该事件后，应该将电影点击数加一
        movie1.click_nums += 1  # movie表
        movie1.save()
        # 点击率最高的电影显示：
        all_movies = Movie.objects.all()
        hot_movies = all_movies.order_by("-click_nums")[:1]
        hot_movie = hot_movies[0]

        # 相关电影推荐，根据标签判断是否相关来推荐，可能为空
        tag = movie1.movie_year_id
        if tag:
            relate_movies = Movie.objects.filter(movie_year=tag)[:5]
        else:
            relate_movies = []
        # 推荐电影集合
        recommendations = movie.recommendations.split(',')

        # 判断是否收藏
        movie_has_fav = False  # 左边的收藏
        hot_has_fav = False  # 右边的收藏
        if request.user.is_authenticated():
            if UserMovie.objects.filter(user=request.user, movie_id=movie1.id):
                movie_has_fav = True
            if UserMovie.objects.filter(user=request.user, movie_id=hot_movie.id):
                hot_has_fav = True

        return render(request, "new_movie_detail.html",
        {
            "movie": movie,
            "movie1": movie1,
            "relate_movies": relate_movies,
            "movie_has_fav": movie_has_fav,
            "hot_movie": hot_movie,
            "hot_has_fav": hot_has_fav,
            "recommendations":recommendations
        })

# 电影用户评论
class MovieCommentView(View):
    def get(self, request, movie_no):
        movie1 = Movie.objects.get(movie_no=movie_no)
        movie2 = MovieDetail.objects.get(movie_no=movie_no)
        movie_id = movie1.id
        all_comments = MovieComments.objects.all().filter(movie_id=movie_id).order_by("-likenum")
        # 相关电影推荐，根据用户收藏表内容来判断是否相关来推荐，可能为空
        id = Movie.objects.get(movie_no=movie_no).id
        users = UserMovie.objects.filter(movie_id=id)  # 找出收藏该电影的记录
        # 取十个电影进行显示
        relate_movies = []
        for user in users:
            user_movies = UserMovie.objects.filter(user_id=user.user_id)  # 找出这些用户收藏的电影
            for user_movie in user_movies:  # 将这些电影加入推荐目录
                relate_movie = Movie.objects.get(id=user_movie.movie_id)
                print (relate_movie.movie_name)
                relate_movies.append(relate_movie)
        relate_movies = set(relate_movies[:10])
        # print (relate_movies)
        return render(request, "new_movie_comment.html", {
            "movie1": movie1,
            "movie2": movie2,
            "all_comments": all_comments,
            "relate_movies": relate_movies
        })

# 用户添加电影评论
class AddMovieCommentView(View):
        def post(self, request):
            if not request.user.is_authenticated():
                return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
            movie_no = request.POST.get('movie_no', '')
            comments = request.POST.get('comments', '')
            if movie_no and comments:
                movie_comments = MovieComments()
                movie = Movie.objects.get(movie_no=movie_no)
                movie_comments.movie = movie
                movie_comments.comments = comments
                movie_comments.user = request.user
                movie_comments.save()
                return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":" 添加失败"}', content_type='application/json')

# 更新likenum
class LikenumView(View):
    def post(self, request):
        print ("点赞数加一")
        movie_id = request.POST.get('movie_id', 0)
        user_id = request.POST.get('user_id', 0)
        comment_id = request.POST.get('comment_id', 0)
        moviecomment = MovieComments.objects.get(user_id=int(user_id), movie_id=int(movie_id), id=int(comment_id))
        moviecomment.likenum += 1
        moviecomment.save()
        return HttpResponse('{}', content_type='application/json')

# 更新dislikenum
class DislikenumView(View):
    def post(self, request):
        print ("点踩数加一")
        movie_id = request.POST.get('movie_id', 0)
        user_id = request.POST.get('user_id', 0)
        comment_id = request.POST.get('comment_id', 0)
        moviecomment = MovieComments.objects.get(user_id=int(user_id), movie_id=int(movie_id), id=int(comment_id))
        moviecomment.dislikenum += 1
        moviecomment.save()
        return HttpResponse('{}', content_type='application/json')
#  收藏与取消收藏功能
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
        fav_id = Movie.objects.get(movie_no=fav_no).id
        fav_type = request.POST.get('fav_type', "")
        print fav_id
        print fav_type
        # 在用户未登录的情况下，python django内置的一个user类，通过is_authenticated()方法来判断是否 处于登陆状态
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
            # AJAX来控制跳转到登陆界面
        movie = Movie.objects.get(movie_no=fav_no)
        moviedetail = MovieDetail.objects.get(movie_no=fav_no)
        exist_record = UserMovie.objects.filter(user=request.user, movie_id=int(fav_id))
        if exist_record:
            # 记录已经存在，则表示用户想要取消收藏
            # 收藏数减一
            movie.fav_nums -= 1
            movie.save()
            moviedetail.fav_nums -= 1
            moviedetail.save()

            exist_record.delete()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:

            user_fav = UserMovie()
            # 若fav_id为0，说明并没有点击收藏
            if int(fav_id) > 0 and fav_type:
                user_fav.user = request.user
                user_fav.movie_id = int(fav_id)
                user_fav.save()
                # 收藏数加一
                movie.fav_nums += 1
                movie.save()
                moviedetail.fav_nums += 1
                moviedetail.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')