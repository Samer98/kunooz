from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('AdditionalModification', views.AdditionalModificationViewSet,basename="AdditionalModification")
router.register('AdditionalModificationComment', views.AdditionalModificationCommentViewSet,basename="AdditionalModificationComment")

urlpatterns = [
              ] + router.urls
