from rest_framework import serializers
from .models import AdditionalModification

class AdditionalModificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = AdditionalModification
        fields = ['id','project','comment','file']

