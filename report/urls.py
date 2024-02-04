from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('Report', views.ReportViewSet,basename="Report")
router.register('ReportComment', views.ReportCommentViewSet,basename="ReportComment")

urlpatterns = [
                  path('projects/<int:project_id>/record/<int:pk>/',
                       views.ReportViewSet.as_view({'get': 'record_info', 'put': 'record_info'}),
                       name='report-record-info'),
              ] + router.urls
