# _*_ coding: utf-8 _*_
__author__ = 'wowoqu'
__date__ = '2018/6/2 23:06'
import xadmin
from .models import CourseOrg, CityDict, Teacher


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_num', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'click_num', 'fav_nums', 'image', 'address', 'city__name', 'add_time']


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                    'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                   'add_time']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
