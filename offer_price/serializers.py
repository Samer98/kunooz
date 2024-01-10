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
            return {
                'id': obj.user.id,
                'first_name': obj.user.first_name,
                'phone_number': str(obj.user.phone_number)
            }
        return None
