from django.contrib import admin
from .models import PricingTender,PricingTenderContractor,OfferPrice

# Register your models here.

admin.site.register(PricingTenderContractor)
admin.site.register(PricingTender)
admin.site.register(OfferPrice)
