from django.contrib import admin
from .models import Approval, ApprovalComment


# Register your models here.

admin.site.register(Approval)
admin.site.register(ApprovalComment)
