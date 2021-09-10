from django.contrib import admin
from .models import Banner, Setting
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

class SettingAdmin(SummernoteModelAdmin):
    list_display = ['website_name', 'address', 'mobile1', 'mobile2', 'email']
    list_display_links = ('website_name',)
    summernote_fields = ('privacy_policy', 'terms_condition', 'refund_policy',)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Banner)