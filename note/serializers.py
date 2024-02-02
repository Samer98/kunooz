from rest_framework import serializers
from .models import Note, NoteComment

class NoteSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Note
        fields = ['id','project','user','title','note','file','date_created']

    def get_user(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            user_data = {
                'id': request.user.id,
                'first_name': request.user.first_name,
                'second_name': request.user.second_name,
                'job_name': request.user.job_name if request.user.job_name else None,
                'profile_picture': request.user.profile_picture.url if request.user.profile_picture else None,
                'role': str(request.user.role),
                'phone_number': str(request.user.phone_number)
            }
            return user_data
        return None

class NoteCommentSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = NoteComment
        fields = ['id','user','note','file','comment','date_created']

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
