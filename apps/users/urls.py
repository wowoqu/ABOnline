# _*_ coding: utf-8 _*_
__author__ = 'wowoqu'
__date__ = '2018/6/28 15:56'

from django.conf.urls import url, include
from .views import UserHomeView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, \
    MyFavOrgView

app_name = 'users'
urlpatterns = [
    url(r'^home/$', UserHomeView.as_view(), name='user_home'),
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    url(r'sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
    url(r'update_email/$', UpdateEmailView.as_view(), name='update_email'),
    # 我的课程
    url(r'mycourse/$', MyCourseView.as_view(), name='my_course'),
    # 我的课程收藏
    url(r'myfavorg/$', MyFavOrgView.as_view(), name='my_favorg'),
]
