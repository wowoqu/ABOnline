from django.http import HttpResponse
from django.shortcuts import render, render_to_response

from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import Course, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
from organization.models import Teacher
from django.db.models import Q


# Create your views here.
class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-click_num')[:3]

        keyword = request.GET.get('keyword', '')
        if keyword:
            all_courses = all_courses.filter(
                Q(name__icontains=keyword) | Q(desc__icontains=keyword) | Q(detail__icontains=keyword))

        # 排序
        order = request.GET.get('order', '')
        if order == 'student':
            all_courses = all_courses.order_by('-students')
        elif order == 'hot':
            all_courses = all_courses.order_by('-click_num')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 10, request=request)

        course = p.page(page)
        all_courses = course
        return render_to_response('course_list.html', locals())


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_num += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_course = Course.objects.filter(tag=tag)[:1]
        else:
            relate_course = []
        return render_to_response('course-detail.html', locals())


class CourseVedioView(LoginRequiredMixin, View):
    def get(self, request, course_id):

        course = Course.objects.get(id=int(course_id))

        # 查询用户是否已经关联了课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学过这门课程的所有同学还学过其他的课程(相关推荐)
        user_courses = UserCourse.objects.filter(course=course)
        # python 列表式 获取所有用户对应的id
        if user_courses:
            user_ids = [user_course.user_id for user_course in user_courses]
            # 两个下划线加in(django model的用法) 表示user_id在后面的列表中的都返回过来，即获取所有的用户课程对应关系
            all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
            # 通过user_id获取所有课程id
            course_ids = [user_course.course_id for user_course in all_user_courses]
            relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]

        all_comments = course.coursecomments_set.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_comments, 5, request=request)

        all_comments = p.page(page)
        return render_to_response('course-vedio.html', locals())


class AddComment(View):
    def post(self, request):
        # 无论是否登陆request中都是由user字段的
        if request.user.is_authenticated:
            course_id = int(request.POST.get('course_id', 0))
            comments = request.POST.get('comments', '')
            if comments and course_id > 0:
                course_comments = CourseComments()
                course = Course.objects.get(id=int(course_id))
                course_comments.course = course
                course_comments.comments = comments
                course_comments.user = request.user
                course_comments.save()
                return HttpResponse(
                    '{"status": "success", "msg": "评论成功"}',
                    content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "评论出错"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "用户未登陆"}', content_type='application/json')


class VideoPlayView(View):
    """
    视频播放页面
    """

    def get(self, request, video_id):

        video = Video.objects.get(id=int(video_id))

        course = video.lesson.course

        # 查询用户是否已经关联了课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 学过这门课程的所有同学还学过其他的课程(相关推荐)
        user_courses = UserCourse.objects.filter(course=course)
        # python 列表式 获取所有用户对应的id
        if user_courses:
            user_ids = [user_course.user_id for user_course in user_courses]
            # 两个下划线加in(django model的用法) 表示user_id在后面的列表中的都返回过来，即获取所有的用户课程对应关系
            all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
            # 通过user_id获取所有课程id
            course_ids = [user_course.course_id for user_course in all_user_courses]
            relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_num')[:5]

        all_comments = course.coursecomments_set.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_comments, 5, request=request)

        all_comments = p.page(page)
        # return render_to_response('course-vedio.html', locals())

        return render_to_response('video_play.html', locals())


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teacher_count = all_teachers.count()
        hot_teacher = all_teachers.order_by('-click_nums')[:3]

        keyword = request.GET.get('keyword', '')
        if keyword:
            all_teachers = all_teachers.filter(name__icontains=keyword)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_teachers = all_teachers.order_by('-click_nums')

        p = Paginator(all_teachers, 5, request=request)

        all_teachers = p.page(page)
        return render_to_response('course_teacher.html', locals())


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = teacher.course_set.all()

        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=int(teacher_id)):
            has_teacher_faved = True
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=int(teacher.org.id)):
            has_org_faved = True

        # 讲师排名
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        return render_to_response('teacher_detail.html', locals())
