# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/14 23:20'

from django import forms
from .models import UserProfile


# 第三方库：验证码
from captcha.fields import CaptchaField
# 登陆表单填写的信息
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5) # 最短长度是5
# 注册表单填写的信息
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})  # 验证码
# 找回密码进行验证时填写的信息
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})  # 验证码
# 找回密码重新填写密码时填写的信息
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

# 用户头像表单提交
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile()
        fields = ['image']

# 用户个人信息表单提交
class UploadMesForm(forms.ModelForm):
    class Meta:
        model = UserProfile()
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']