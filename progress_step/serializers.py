from rest_framework import serializers
from .models import ProgressStep, ProgressStepComment


class ProgressStepSerializers(serializers.ModelSerializer):
    order = serializers.IntegerField(read_only=True)
    sub_steps = serializers.SerializerMethodField(read_only=True)

    # sub_steps_comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ProgressStep
        fields = ['id', 'title', 'project', "parent", "order", "is_finished", 'sub_steps']

    def get_sub_steps(self, obj):
        sub_steps = ProgressStep.objects.filter(parent=obj)
        if sub_steps.exists():
            serializer = ProgressStepSerializers(sub_steps, many=True, context=self.context)

            # Check if there are comments for each sub-step
            for sub_step_data in serializer.data:
                sub_step_instance = ProgressStep.objects.get(id=sub_step_data['id'])
                comments = ProgressStepComment.objects.filter(sub_step=sub_step_instance)
                if comments.exists():
                    comment_serializer = ProgressStepCommentSerializers(comments, many=True)
                    sub_step_data['sub_steps_comments'] = comment_serializer.data
                else:
                    sub_step_data['sub_steps_comments'] = None

            return serializer.data
        return None


class ProgressStepCommentSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProgressStepComment
        fields = ['id', 'user', 'sub_step', 'file', 'comment', 'date_created']

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
