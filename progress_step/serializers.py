from rest_framework import serializers
from .models import ProgressStep, ProgressStepComment



class ProgressStepSerializers(serializers.ModelSerializer):
    order = serializers.IntegerField(read_only=True)
    class Meta:
        model = ProgressStep
        fields = ['id','title','project',"parent","order"]


class ProgressStepCommentSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.CharField(read_only=True)
    class Meta:
        model = ProgressStepComment
        fields = ['id','user','additional_modification','file','comment','date_created']
