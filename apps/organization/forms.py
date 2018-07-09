# _*_ coding: utf-8 _*_
__author__ = 'wowoqu'
__date__ = '2018/6/16 12:53'
import re
from django import forms
from operation.models import UserAsk


# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     phone = forms.CharField(required=True, min_length=11, max_length=11)
#     course_num = forms.CharField(required=True, min_length=5, max_length=50)


# 继承ModelForm类，可以直接保存
class UserAskForm(forms.ModelForm):
    # # 新增字段
    # my_field = forms.CharField()
    class Meta:
        # 指明继承的model
        model = UserAsk
        # 指明需要的model中的字段
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        # 验证手机号码是否合法
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1[358]\d{9}$ |^147\d{8}$|^176\d{8}$|^166\d{8}$|^159\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')
