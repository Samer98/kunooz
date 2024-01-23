from rest_framework import serializers
from .models import OfferPrice, OfferPriceComment

class OfferPriceSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)

    class Meta:
        model = OfferPrice
        fields = ['id', 'project', 'title', 'project_duration', 'bid_price', 'note', 'file', 'date_created']


class OfferPriceCommentSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OfferPriceComment
        fields = ['id','user','offer_price','file','comment','date_created']

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
