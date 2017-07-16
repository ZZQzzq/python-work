# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/18 11:04'


from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from Crawler.settings import EMAIL_FROM

# 生成随机字符串code,发给邮箱的验证码
def random_str(randomlength=8):
    str = ''
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxxyz0123456789'
    length = len(chars)
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str
# 给注册用户发送邮件
def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""
    if send_type == "register":  # 发送注册链接
        email_title = "爬虫在线网激活链接"
        email_body = "咳咳！ \n" \
                     "请点击下面链接激活“>_<胖球”的账号：\n" \
                     "http://127.0.0.1:8080/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 返回结果是一个bool值
        if send_status:
            pass
    elif send_type == "forget":  # 发送重置密码链接
        email_title = "爬虫在线网密码重置链接"
        email_body = "请点击下面链接激活你的账号：\n" \
                     "http://127.0.0.1:8080/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 返回结果是一个bool值
        if send_status:
            pass

    elif send_type == "update_email":  # 发送重置密码链接
        email_title = "爬虫在线网密邮箱修改验证码链接"
        email_body = "你的邮箱验证码为:{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 返回结果是一个bool值
        if send_status:
            pass
