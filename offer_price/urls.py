from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('OfferPrice', views.OfferPriceViewSet,basename="OfferPrice")
router.register('OfferPriceComment', views.OfferPriceCommentViewSet,basename="OfferPriceComment")

urlpatterns = [
              ] + router.urls
