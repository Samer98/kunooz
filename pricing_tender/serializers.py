from rest_framework import serializers
from .models import PricingTender,PricingTenderContractor ,OfferPrice

class PricingTenderContractorSerializers(serializers.ModelSerializer):
    member_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    member_role = serializers.SerializerMethodField()

    class Meta:
        model = PricingTenderContractor
        fields = ['id','pricing_tender','member','member_name','phone_number','member_role']

    def get_member_name(self, obj):
        return obj.member.first_name if obj.member.first_name else 'No Name'

    def get_member_role(self, obj):
        return str(obj.member.role)
    def get_phone_number(self, obj):
        return str(obj.member.phone_number)
class PricingTenderSerializers(serializers.ModelSerializer):
    members = PricingTenderContractorSerializers(many=True, source='pricingtendercontractor_set', read_only=True)
    pricing_tender_owner = serializers.CharField(read_only=True)
    date_created = serializers.DateField(read_only=True)

    class Meta:
        model = PricingTender
        fields = ['id','pricing_tender_owner','project_name','planing','three_d',
                  'quantities_and_specifications','other_files','members', 'date_created']


# class PricingTinderCommentSerializers(serializers.ModelSerializer):
#     date_created = serializers.DateField(read_only=True)
#     user = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = PricingTinderComment
#         fields = ['id','user','pricing_tender','file','comment','date_created']


class OfferPriceSerializers(serializers.ModelSerializer):
    date_created = serializers.DateField(read_only=True)

    class Meta:
        model = OfferPrice
        fields = ['id', 'project', 'title', 'project_duration', 'bid_price', 'note', 'file', 'date_created']
