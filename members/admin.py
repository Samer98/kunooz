from django.contrib import admin
from django.contrib.auth.admin import  UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Role
# Register your models here.


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name','second_name' )}),
        (_('Employee info'), {'fields': (
        'company_name', 'introduction','services','projects_limits')}),
        (_('Permissions'), {'fields': ('role','is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2','first_name','second_name','services'),
        }),
    )
    list_display = ('id',"phone_number", 'first_name','second_name','is_staff')
    search_fields = ('phone_number', 'first_name', )
    ordering = ('phone_number',)


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Role)
# @admin.register(Consultant)
# class ConsultantAdmin(admin.ModelAdmin):
#     list_display = ['email','full_name','job_name']
