from rest_framework import serializers
from .models import Project,Project_members
class ProjectSerializers(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id','title','project_number','style','room_number','space','location',
                  "outer_design",'total_budget',"start_date","end_date","status"]