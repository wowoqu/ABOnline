# _*_ coding: utf-8 _*_
__author__ = 'wowoqu'
__date__ = '2018/6/18 23:13'

from django.conf.urls import url, include
from .views import CourseListView, CourseDetailView, CourseVedioView, AddComment, VideoPlayView, TeacherListView, \
    TeacherDetailView


app_name = 'courses'
urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^vedio/(?P<course_id>\d+)/$', CourseVedioView.as_view(), name='course_vedio'),
    url(r'^add_comments/$', AddComment.as_view(), name='add_comments'),
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),
    url(r'^teacher/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
]
