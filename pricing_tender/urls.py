from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('PricingTender', views.PricingTenderViewSet,basename="PricingTender")
# router.register('PricingTenderComment', views.PricingTinderCommentViewSet,basename="PricingTenderComment")

urlpatterns = [
              ] + router.urls
