"""moocweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

from account import views as account_views
from organization import views as organization_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="index"),
    url(r'^login/$', account_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', account_views.user_logout, name='logout'),
    url(r'^register/$', account_views.RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', account_views.ActiveUserView.as_view(), name="active"),
    url(r'^forget/', account_views.ForgetPasswordView.as_view(), name="forget_password"),
    url(r'^reset/(?P<reset_code>.*)/$', account_views.ResetPasswordView.as_view(), name="reset_password"),
    url(r'^modify/$', account_views.ModifyPasswordView.as_view(), name="modify_password"),
    # 添加课程机构app的urls
    url(r'^org/', include('organization.urls', namespace="org")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 配置media上传文件也可以使用
# from django.views.static import serve
# url(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT} )