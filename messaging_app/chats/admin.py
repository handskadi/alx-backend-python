from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import users


admin.site.register(users, UserAdmin)
