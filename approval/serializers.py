from rest_framework import serializers
from .models import Approval, ApprovalComment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ApprovalSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    class Meta:
        model = Approval
        fields = ['id','project','title','note','file','date_created']


class ApprovalCommentSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ApprovalComment
        fields = ['id','user','approval','file','comment','date_created']

    def get_user(self, obj):
        if obj.user:
            return {
                'id': obj.user.id,
                'first_name': obj.user.first_name,
                'phone_number': str(obj.user.phone_number)
            }
        return None
