from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('Approval', views.ApprovalViewSet,basename="Approval")
router.register('ApprovalComment', views.ApprovalCommentViewSet,basename="ApprovalComment")

urlpatterns = [
              ] + router.urls
