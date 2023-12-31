from rest_framework import serializers
from .models import ProgressStep, ProgressStepComment



class ProgressStepSerializers(serializers.ModelSerializer):
    order = serializers.IntegerField(read_only=True)
    class Meta:
        model = ProgressStep
        fields = ['id','title','project',"parent","order","is_finished"]


class ProgressStepCommentSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ProgressStepComment
        fields = ['id','user','sub_step','file','comment','date_created']

    def get_user(self, obj):
        if obj.user:
            return {
                'id': obj.user.id,
                'first_name': obj.user.first_name,
                'phone_number': str(obj.user.phone_number)
            }
        return None