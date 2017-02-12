# _*_ coding:utf-8 _*_
from django.contrib import admin

from .models import UserProfile, EmailVerifyRecord, Banner

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active']
    search_fields = ['username', 'email']
    list_filter = ['is_active']

class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['send_type', 'send_time']

class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'add_time', 'index']

admin.site.register(UserProfile, UserProfileAdmin)

admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
admin.site.register(Banner, BannerAdmin)
