# _*_ coding: utf-8 _*_
from users.models import UserProfile

__author__ = 'wowoqu'
__date__ = '2018/6/4 8:28'
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    username = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField()
    # captcha = CaptchaField(error_messages={'invilde': '验证码错误'})


class ForgetForm(forms.Form):
    username = forms.EmailField(required=True)
    captcha = CaptchaField()


class ModifyPwdForm(forms.Form):
    password = forms.CharField(required=True, min_length=5)
    re_password = forms.CharField(required=True, min_length=5)


class UploadImgForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UpdateEmailForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']
