# _*_ coding: utf-8 _*_
from random import Random
from ABOnline.settings import EMAIL_FROM
from django.http import HttpResponse

__author__ = 'wowoqu'
__date__ = '2018/6/8 20:55'

from users.models import EmailVerifyRecord
from django.core.mail import send_mail


# 创建要发送的字符串并保存到数据库中
def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'reemail':
        code = generate_random_str(6)
    else:
        code = generate_random_str(16)
    email_record.core = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 定义要发送邮件的正文
    email_title = ''
    email_body = ''
    # 判断是注册还是忘记密码
    if send_type == 'register':
        email_title = 'ABOline注册激活链接'
        email_body = '请点击下面的链接激活你的账号：127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status
    elif send_type == 'forget':
        email_title = 'ABOline密码找回链接'
        email_body = '请点击下面的链接找回你的密码：127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status
    elif send_type == 'reemail':
        email_title = 'ABOline在线修改邮箱验证码'
        email_body = '你的邮箱验证码为：{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        return send_status


def generate_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str
