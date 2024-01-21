from rest_framework import serializers
from .models import ProgressStep, ProgressStepComment



class ProgressStepSerializers(serializers.ModelSerializer):
    order = serializers.IntegerField(read_only=True)
    sub_steps = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ProgressStep
        fields = ['id','title','project',"parent","order","is_finished",'sub_steps']

    def get_sub_steps(self, obj):
        sub_steps = ProgressStep.objects.filter(parent=obj)
        if sub_steps.exists():
            serializer = ProgressStepSerializers(sub_steps, many=True)
            return serializer.data
        return None



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