from rest_framework import serializers
from .models import Report, ReportComment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ReportSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    class Meta:
        model = Report
        fields = ['id','project','worker_name','note','file','date_created']

class ReportCommentSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ReportComment
        fields = ['id','user','report','file','comment','date_created']

    def get_user(self, obj):
        if obj.user:
            return {
                'id': obj.user.id,
                'first_name': obj.user.first_name,
                'phone_number': str(obj.user.phone_number)
            }
        return None
