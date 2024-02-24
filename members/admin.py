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
        (_('Personal info'), {'fields': ('first_name','second_name','profile_picture',"cv","Commercial_license" )}),
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
    list_display = ('id',"phone_number", 'first_name','second_name','is_staff','role')
    search_fields = ('phone_number', 'first_name', )
    ordering = ('phone_number',)


admin.site.register(get_user_model(), CustomUserAdmin)


# class RoleAdmin(admin.ModelAdmin):
#

# Register the Role model with the custom admin class
# admin.site.register(Role, RoleAdmin)
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'role']

    def has_add_permission(self, request):
        # Prevent adding new roles
        return False

    def has_delete_permission(self, request, obj=None):
        # Prevent deleting existing roles
        return False

    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly
        if obj:
            return [field.name for field in self.model._meta.fields]
        return []