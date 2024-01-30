from rest_framework import serializers
from .models import Project,ProjectMember

class ProjectMembersSerializers(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    class Meta:
        model = ProjectMember
        fields = ['id','project','member','member_name','phone_number']

    def get_member_name(self, obj):
        return obj.member.first_name if obj.member.first_name else 'No Name'
    def get_phone_number(self, obj):
        return str(obj.member.phone_number)
class ProjectSerializers(serializers.ModelSerializer):
    # project_owner = serializers.CharField(max_length=255,read_only=True)
    members = ProjectMembersSerializers(many=True, source='projectmember_set', read_only=True)
    project_owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = ['id','title','project_number','project_owner','style','room_number','space','location',
                  "outer_design",'total_budget',"start_date","end_date","status",'members']

    def get_project_owner(self, obj):
        if obj.project_owner:
            user_data = {
                'id': obj.project_owner.id,
                'first_name': obj.project_owner.first_name,
                'second_name': obj.project_owner.second_name,
                # 'profile_picture': obj.project_owner.profile_picture.url if obj.project_owner.profile_picture else None,
                # 'role': str(obj.project_owner.role),
                # 'phone_number': str(obj.project_owner.phone_number)
            }
            return user_data
        return None
