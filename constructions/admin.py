from django.contrib import admin
from .models import Project,ProjectMember
# Register your models here.

# admin.site.register(Project)
# admin.site.register(ProjectMember)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','project_owner','status']
    list_editable = ['status']


@admin.register(ProjectMember)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'project','member']
