import json

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.template import RequestContext

from .models import UserProfile, EmailVerifyRecord
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImgForm, UpdateEmailForm
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        # hash_key = CaptchaStore.generate_key()
        # image_url = captcha_image_url(hash_key)
        return render(request, 'register.html', locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            all_user = UserProfile.objects.filter(username=user_name)
            if all_user:
                return render(request, 'register.html', {'msg': '用户名已存在', 'register_form': register_form})
            else:
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.is_active = False
                user_profile.password = make_password(pass_word)
                user_profile.save()
                status = send_register_email(user_name, 'register')
                if status:
                    return HttpResponse('<h1>邮箱已发送请前往激活</h1>')
                else:
                    return HttpResponse('<h1>邮箱发送失败</h1>')
                # return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(core=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
            return render(request, 'login.html')
        else:
            return HttpResponse('<h1>链接不存在</h1>')


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(core=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return HttpResponse('<h1>链接不存在</h1>')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get('email', '')
            pwd = request.POST.get('password', '')
            re_pwd = request.POST.get('re_password', '')
            if pwd != re_pwd:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(re_pwd)
            user.save()
            return render(request, 'login.html', {})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)  # 创建实例
        if login_form.is_valid():
            user_name = request.POST.get('username')
            pass_word = request.POST.get('password')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render_to_response('index.html', locals())
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码不正确'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def refresh_captcha(request):
    to_json_response = dict()
    to_json_response['status'] = 1
    to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
    to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])
    return HttpResponse(json.dumps(to_json_response), content_type='application/json')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forget_pwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('username', '')
            status = send_register_email(email, 'forget')
            if status:
                return HttpResponse('<h1>邮箱已发送, 请查收</h1>')
            else:
                return render(request, 'forget_pwd.html', {'msg': '邮箱发送失败'})
        else:
            return render(request, 'forget_pwd.html', {'forget_form': forget_form})


class UserHomeView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        current_page = 'home'
        return render(request, 'user_home.html', locals())

    def post(self, request):
        upemail_form = UpdateEmailForm(request.POST, instance=request.user)
        if upemail_form.is_valid():
            upemail_form.save()
            return HttpResponse('{"status": "success", "msg":"个人主页修改成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail","msg":"用户输入不正确"}', content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """用户修改头像"""

    def post(self, request):
        # instance 实例化对象 传递的是ModelForm对象 当前form具备form的功能
        image_form = UploadImgForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # request.user.image = image_form.cleaned_data['image']
            # request.user.save()
            # 因为它具有form功能 所以不需要赋值，可直接保存
            image_form.save()
            # return render(request, 'user_home.html', locals())
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail"}', content_type='application/json')


class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd = request.POST.get('password', '')
            re_pwd = request.POST.get('re_password', '')
            if pwd != re_pwd:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(re_pwd)
            user.save()
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """

    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_register_email(email, 'reemail')
        return HttpResponse('{"status": "success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """修改个人邮箱"""

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_record = EmailVerifyRecord.objects.filter(email=email, core=code, send_type='reemail')
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"email":"修改邮箱成功"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')

# Create your views here.
# 函数形式的login
# def user_login(req):
#     if req.method == 'POST':
#         user_name = req.POST.get('user')
#         pass_word = req.POST.get('passwd')
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(req, user)
#             return render_to_response('index.html', locals())
#             pass
#             # return render(req, 'index.html')
#         else:
#             return render(req, 'login.html', {})
#     elif req.method == 'GET':
#         return render(req, 'login.html', {})
