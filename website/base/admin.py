from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Entry, Group, GroupMember

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'employee_number', 'region', 'department', 'is_staff')


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Entry)
admin.site.register(Group)
admin.site.register(GroupMember)