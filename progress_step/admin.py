from django.contrib import admin
from .models import  ProgressStep, ProgressStepComment
# Register your models here.

@admin.register(ProgressStep)
class ProgressStepAdmin(admin.ModelAdmin):
    list_display = ['id', 'title','project','display_parent_id']

    def display_parent_id(self, obj):
        if obj.parent:
            return obj.parent.id
        return None

    display_parent_id.short_description = 'Parent ID'


# @admin.register(ProgressStepComment)
# class ProgressStepCommentAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title','project_owner','status']
#     list_editable = ['status']
