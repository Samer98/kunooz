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
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = AdditionalModificationComment
        fields = ['id','user','additional_modification','file','comment','date_created']

    def get_user(self, obj):
        if obj.user:
            user_data = {
                'id': obj.user.id,
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name,
                'profile_picture': obj.user.profile_picture.url if obj.user.profile_picture else None,
                'role': str(obj.user.role),
                'phone_number': str(obj.user.phone_number)
            }
            return user_data
        return None
