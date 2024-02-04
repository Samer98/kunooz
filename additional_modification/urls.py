from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('AdditionalModification', views.AdditionalModificationViewSet,basename="AdditionalModification")
router.register('AdditionalModificationComment', views.AdditionalModificationCommentViewSet,basename="AdditionalModificationComment")


urlpatterns = [
                  path('projects/<int:project_id>/record/<int:pk>/',
                       views.AdditionalModificationViewSet.as_view({'get': 'record_info', 'put': 'record_info'}),
                       name='report-record-info'),
              ] + router.urls
