from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.generic.base import View
from .models import CourseOrg, CityDict
from .forms import UserAskForm
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from courses.models import Course
from operation.models import UserFavorite


# Create your views here.
class OrganizationInView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_num')[:3]  # 课程机构排名
        all_citys = CityDict.objects.all()

        keyword = request.GET.get('keyword', '')
        if keyword:
            all_orgs = all_orgs.filter(
                Q(name__icontains=keyword) | Q(desc__icontains=keyword))

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            # 虽然在定义表中为city字段，但在数据库中的字段名字为city_id
            all_orgs = all_orgs.filter(city_id=city_id)

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(catgory=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)
        org_nums = all_orgs.count()
        orgs = p.page(page)
        all_orgs = orgs

        return render_to_response('organization_class.html', locals())
        # return render(request, 'organization_class.html', {})


class AddUserAskView(View):

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)  # commit=True才会保存到数据库中
            # return HttpResponse("{'status': 'success'}", content_type='application/json')
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "错误"}',
                                content_type='application/json')


class OrgBaseView(View):
    def get(self, request):
        return render_to_response('index_base.html', locals())


class OrgHomeView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        current_page = 'home'
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render_to_response('index_base.html', locals())


class OrgCourseView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 4, request=request)
        orgs = p.page(page)
        all_courses = orgs
        current_page = 'course'
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render_to_response('org_course.html', locals())


class OrgDescView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'desc'
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render_to_response('org_desc.html', locals())


class OrgTeacherView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        current_page = 'teacher'
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render_to_response('org_teacher.html', locals())


class AddFavView(View):
    # 用户收藏，取消收藏
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 无论是否登陆request中都是由user字段的
        if request.user.is_authenticated:
            exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if exist_records:
                # 如果记录已经存在 则取消收藏
                exist_records.delete()
                return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
            else:
                user_fav = UserFavorite()
                if int(fav_id) > 0 and int(fav_type) > 0:
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()
                    return HttpResponse('{"status": "success", "msg": "收藏成功"}', content_type='application/json')
                else:
                    return HttpResponse('{"status": "fail", "msg": "收藏出错"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "用户未登陆"}', content_type='application/json')




