# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/18 13:08'

import re
from django import forms


# class UserAskForm(forms.ModelForm):
#     class Meta:
#         model = UserAsk
#         fields = ['name', 'mobile', 'course_name']
#     # 验证手机号码是否合法（11位）
#     def clean_mobile(self):   # 必须以clean_开头，程序遇到mobile字段就会自动跳入这个函数进行判断
#         mobile = self.cleaned_data['mobile']  # clean_data表示已经取出来了数据，字典类型
#         REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"  # 手机号码正则匹配
#         p = re.compile(REGEX_MOBILE)
#         if p.match(mobile):  # 手机号码合法，则返回手机号
#             return mobile
#         else:  # 否则抛出异常
#              raise forms.ValidationError(u"手机号法非法",code="mobile_invalid" )

# 用户查询
class UserAskForm(forms.Form):
    book_name = forms.CharField(max_length=50)
    book_type = forms.CharField(max_length=5)
    book_star = forms.FloatField()

