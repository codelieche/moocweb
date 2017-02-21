# _*_ coding:utf-8 _*_

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):
    '''为View类提供的登陆控制类'''

    @method_decorator(login_required(login_url="/login/"))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

