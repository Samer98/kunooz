from rest_framework import serializers
from .models import Project,ProjectMember
class ProjectSerializers(serializers.ModelSerializer):
    project_owner = serializers.CharField(max_length=255,read_only=True)
    class Meta:
        model = Project
        fields = ['id','title','project_number','project_owner','style','room_number','space','location',
                  "outer_design",'total_budget',"start_date","end_date","status"]

class ProjectMembersSerializers(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id','project','member',"phone_number"]