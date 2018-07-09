# _*_ coding: utf-8 _*_
__author__ = 'wowoqu'
__date__ = '2018/6/25 16:31'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)
