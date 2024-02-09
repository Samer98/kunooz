from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'user','type', 'message','extra_data', 'created_at', 'is_read']

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