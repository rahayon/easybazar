from django.contrib import admin
from accounts.models import CustomUser
from accounts.models import UserProfile
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(CustomUser)
admin.site.site_header = "EasyBazar Admin"
admin.site.site_title = "EasyBazar Admin Portal"
admin.site.index_title = "Welcome to EasyBazar"
