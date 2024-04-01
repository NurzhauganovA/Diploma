from django.contrib import admin

from .models import User, UserInfo


admin.site.register(User)
admin.site.register(UserInfo)
