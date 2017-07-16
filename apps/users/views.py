# -*- coding:utf-8 -*-
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View

from book.models import Book, BookDetail
from movies.models import Movie, MovieDetail
from operation.models import UserBook, UserMovie,UserMessage
from utils.email_send import send_register_email
from utils.mixn_utils import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UploadMesForm
from .models import UserProfile, EmailVerifyRecord, Banner


# Create your views here.
# 设置多种登录方式
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)| Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None
# 用户激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")

        return render(request, "login.html")
# 注册
class RegisterView(View):
    # 重写View中的get和post方法
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 注册成功，返回登陆界面
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg": "-o-邮箱已被注册"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False  # 先默认为未激活状态
            user_profile.password = make_password(pass_word)  # 将密码保存成密文形式
            user_profile.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.message = "欢迎注册爬虫在线~~"
            user_message.user = user_profile.id
            user_message.save()
            send_register_email(user_name, "register")
            return render(request, "login.html")
        else:  # 注册失败，返回错误信息并继续停留在注册界面
            return render(request, "register.html", {"register_form": register_form})


    #def post(self, request):
# 登陆
class LoginView(View):
    # 重写View中的get和post方法
    def get(self, request):
        return render(request, "login.html", {})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # 验证成功
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:  # 用户名和密码是否出错
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse  # 专门用于重定向
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": ">_<用户名或密码错误！"})
        else:  # 验证失败,返回错误信息
            return render(request, "login.html", {"login_form": login_form})
# 退出
class LogoutView(View):
    def get(self, request):
        logout(request)
        # 页面重定向HttpResponseRedirect
        from django.core.urlresolvers import reverse  # 专门用于重定向
        return HttpResponseRedirect(reverse("index"))
# 忘记密码
class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():   # 表单验证成功
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})
# 申请密码修改
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")

        return render(request, "login.html")
# 新密码设定
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)  # 设置密码为密文
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})
# 用户个人信息
class UserInfoView(LoginRequiredMixin, View):
    """设置权限，必须用户登录以后才可以访问"""
    # 显示
    def get(self, request):
        sign = "info"
        return render(request, "usercenter-info.html", {
            "sign":sign
        })
    # 信息提交
    def post(self, request):
        user_info_form = UploadMesForm(request.POST, instance=request.user)  # 确定登陆用户是当前用户
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')
# 用户修改头像
class UploadImageView(LoginRequiredMixin, View):
    def post(self,request):
        # 实例化一个image_form
        # 文件类型放在request.FILES中，所以除了POST外，必须上传FILES,Instance将user直接实例化为一个UploadImageForm()对象
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success", "msg":"上传成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"s上传失败"}', content_type='application/json')
# 个人中心用户密码修改
class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)  # 设置密码为密文
            user.save()
            return HttpResponse('{"status":"success", "msg":"密码修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')
# 发送邮箱验证码
class SendEmailView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
             return HttpResponse('{ "email":"邮箱已被注册"}', content_type='application/json')
        send_register_email(email, "update_email")
        return HttpResponse('{ "status":"success"}', content_type='application/json')
# 修改邮箱
class UpdateEmailView(View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        # 判断是否已经发送了验证码，即这条记录是否存在
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        # 如果存在，则修改邮箱并保存
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{ "status":"success"}', content_type='application/json')
        # 否则，返回出错
        else:
            return HttpResponse('{ "email":"验证码出错"}', content_type='application/json')
# 我收藏的图书
class MyFavBookView(LoginRequiredMixin, View):
    def get(self, request):
        book_list = []  # 当前用户的图书收藏表
        fav_books = UserBook.objects.filter(user=request.user)
        for fav_book in fav_books:
            book_id = fav_book.book_id
            book = Book.objects.get(id=book_id)
            book_list.append(book)
        sign = "fav"
        # 对收藏图书进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
        p = Paginator(book_list, 5)
        books = p.page(page)
        return render(request, 'usercenter-fav-book.html', {

            "books": books,
            "sign": sign
        })
# 我收藏的电影
class MyFavMovieView(LoginRequiredMixin, View):
    def get(self, request):
        movie_list = []
        fav_movies = UserMovie.objects.filter(user=request.user)
        for fav_movie in fav_movies:
            movie_id = fav_movie.movie_id
            movie = Movie.objects.get(id=movie_id)
            movie_list.append(movie)
        sign = "fav"
        # 对收藏电影进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
        p = Paginator(movie_list, 5)
        movies = p.page(page)
        return render(request, 'usercenter-fav-movie.html', {

            "movies": movies,
            "sign": sign
        })
# 我的消息
class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        sign = "msg"  # 跳转时的标识
        # 进入该页面后表示未读信息全部被读
        for mess in all_message:
            mess.has_read = True
            mess.save()
        # 对个人消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = 1
        p = Paginator(all_message, 5)
        messages = p.page(page)
        return render(request, "usercenter-message.html", {
            "messages": messages,
            "sign": sign
        })
# 主页显示
class IndexView(View):
    def get(self,request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        # 图书列表
        books = Book.objects.all().order_by("-click_nums")[:6]   # 取6个
        book_banner = Book.objects.order_by("-click_nums")[:3]
        # 电影列表
        movies = Movie.objects.all().order_by("-click_nums")[:6]  # 取6个
        movie_banner = Movie.objects.order_by("-click_nums")[:3]
        return render(request, "index.html",
        {
            "all_banners": all_banners,
            "books": books,
            "book_banner":book_banner,
            "movies": movies,
            "movie_banner": movie_banner
        })
# 404配置
def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404
    return response
# 500配置
def page_error(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html')
    response.status_code = 500
    return response


# (函数实现)页面跳转时的业务逻辑
"""
def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, "login.html", {"msg": ">_<用户名或密码错误！"})
    elif request.method == "GET":  # 把用户页面返回
        return render(request, "login.html", {})"""




