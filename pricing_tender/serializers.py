from rest_framework import serializers
from .models import PricingTender,PricingTenderContractor

class PricingTenderContractorSerializers(serializers.ModelSerializer):
    contractor_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    class Meta:
        model = PricingTenderContractor
        fields = ['id','project','member','contractor_name','phone_number']

    def get_contractor_name(self, obj):
        return obj.member.first_name if obj.member.first_name else 'No Name'
    def get_phone_number(self, obj):
        return str(obj.member.phone_number)
class PricingTenderSerializers(serializers.ModelSerializer):
    members = PricingTenderContractorSerializers(many=True, source='projectmember_set', read_only=True)
    class Meta:
        model = PricingTender
        fields = ['id','project','project_name','planing','three_d',
                  'quantities_and_specifications','other_files''members']

