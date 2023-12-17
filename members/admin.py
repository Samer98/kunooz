from django.contrib import admin
from django.contrib.auth.admin import  UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import User
# Register your models here.


class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name','second_name','personal_date' )}),
        (_('Employee info'), {'fields': (
        'company_name', 'introduction')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2','first_name','second_name'),
        }),
    )
    list_display = ('id', 'first_name','second_name','phone_number', 'is_staff')
    search_fields = ('phone_number', 'first_name', )
    ordering = ('phone_number',)


admin.site.register(get_user_model(), CustomUserAdmin)
# @admin.register(Consultant)
# class ConsultantAdmin(admin.ModelAdmin):
#     list_display = ['email','full_name','job_name']
