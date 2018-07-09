"""ABOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.views.static import serve
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, refresh_captcha, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from organization.views import OrganizationInView, OrgBaseView
from ABOnline.settings import MEDIA_ROOT


urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # url(r'^login/$', TemplateView.as_view(template_name='login.html'), name='login'),
    # url(r'^login/$', user_login, name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^refresh_captcha/', refresh_captcha, name='refresh_captcha'),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify/$', ModifyPwdView.as_view(), name='modify_pwd'),
    # 个人中心
    url(r'^user/', include('users.urls', namespace='users')),
    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程url配置
    url(r'^course/', include('courses.urls', namespace='course')),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    # url(r'^org_base/$', OrgBaseView.as_view(), name='org_base')
]
