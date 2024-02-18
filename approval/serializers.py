from rest_framework import serializers
from .models import Approval, ApprovalComment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ApprovalSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)  # Add this field

    class Meta:
        model = Approval
        fields = ['id','project','user','title','note','file',"comments_count",'date_created']

    def get_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            user_data = {
                'id': request.user.id,
                'first_name': request.user.first_name,
                'second_name': request.user.second_name,
                'job_name': request.user.job_name if request.user.job_name else None,
                'profile_picture': request.user.profile_picture.url if request.user.profile_picture else None,
                'role': str(request.user.role),
                'phone_number': str(request.user.phone_number)
            }
            return user_data
        return None
    def get_comments_count(self, obj):
        return obj.approvalcomment_set.count()

class ApprovalCommentSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ApprovalComment
        fields = ['id','user','approval','file','comment','date_created']

    def get_user(self, obj):
        if obj.user:
            user_data = {
                'id': obj.user.id,
                'first_name': obj.user.first_name,
                'second_name': obj.user.second_name,
                'profile_picture': obj.user.profile_picture.url if obj.user.profile_picture else None,
                'role': str(obj.user.role),
                'phone_number': str(obj.user.phone_number)
            }
            return user_data
        return None
