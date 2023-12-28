from rest_framework import serializers
from .models import Project,ProjectMembers
class ProjectSerializers(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id','title','project_number','project_owner','style','room_number','space','location',
                  "outer_design",'total_budget',"start_date","end_date","status"]

class ProjectMembersSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProjectMembers
        fields = ['id','project_id','user_phone']