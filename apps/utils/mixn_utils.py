# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/24 10:48'
"""
当使用class作为View的逻辑处理，而不是函数时，如何做登录验证，如果用函数是用@login_required
在apps下的utils包中，新建一个文件mixin_utils.py
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)