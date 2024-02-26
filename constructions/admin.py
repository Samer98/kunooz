from django.contrib import admin
from .models import Project,ProjectMember
# Register your models here.

# admin.site.register(Project)
# admin.site.register(ProjectMember)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','project_owner','creation_date','status']
    autocomplete_fields = ['project_owner']
    search_fields = ['phone_number']
    list_editable = ['status']


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'project','member']
