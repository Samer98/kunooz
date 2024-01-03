from rest_framework import serializers
from .models import AdditionalModification , AdditionalModificationComment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class AdditionalModificationSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    class Meta:
        model = AdditionalModification
        fields = ['id','project','title','note','file','date_created']


class AdditionalModificationCommentSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.CharField(read_only=True)
    class Meta:
        model = AdditionalModificationComment
        fields = ['id','user','additional_modification','file','comment','date_created']


