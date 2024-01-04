from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('ApprovalViewSet', views.ApprovalViewSet,basename="AdditionalModification")
router.register('ApprovalCommentViewSet', views.ApprovalCommentViewSet,basename="AdditionalModificationComment")

urlpatterns = [
              ] + router.urls
