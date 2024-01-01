from rest_framework import serializers
from .models import Project,ProjectMember

class ProjectMembersSerializers(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()
    class Meta:
        model = ProjectMember
        fields = ['id','project','member','member_name']

    def get_member_name(self, obj):
        return obj.member.first_name if obj.member.first_name else 'No Name'
class ProjectSerializers(serializers.ModelSerializer):
    project_owner = serializers.CharField(max_length=255,read_only=True)
    members = ProjectMembersSerializers(many=True, source='projectmember_set', read_only=True)
    class Meta:
        model = Project
        fields = ['id','title','project_number','project_owner','style','room_number','space','location',
                  "outer_design",'total_budget',"start_date","end_date","status",'members']

