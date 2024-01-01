from rest_framework import serializers
from .models import AdditionalModification

class AdditionalModificationSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    class Meta:
        model = AdditionalModification
        fields = ['id','project','title','note','file','date_created']

