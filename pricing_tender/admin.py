from django.contrib import admin
from .models import PricingTender, PricingTenderContractor, OfferPrice


# Register your models here.

@admin.register(PricingTenderContractor)
class PricingTenderContractorAdmin(admin.ModelAdmin):
    list_display = ('id', 'pricing_tender', 'member')  # Add other fields you want to display


@admin.register(PricingTender)
class PricingTenderAdmin(admin.ModelAdmin):
    list_display = ('id', 'pricing_tender_owner', 'project_name', 'planing',
                    'three_d', 'quantities_and_specifications')  # Add other fields you want to display


@admin.register(OfferPrice)
class OfferPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'pricing_tender', 'title', "project_duration", 'bid_price')
