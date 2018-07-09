# _*_ coding: utf-8 _*_
import xadmin
from .models import EmailVerifyRecord, Banner
from xadmin import views

__author__ = 'wowoqu'
__date__ = '2018/6/2 21:20'


class BaseSetting(object):
    # 设置主题
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '奥本后台管理系统'
    site_footer = '奥本在线网'
    menu_style = 'accordion'  # 折叠app 将app下面的表折叠起来


class EmailVerifyRecordAdmin(object):
    list_display = ['core', 'email', 'send_type', 'send_time']
    search_fields = ['core', 'email', 'send_type']
    list_filter = ['core', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)  # 设置title和footer
