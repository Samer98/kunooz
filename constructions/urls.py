from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('project', views.ProjectViewSet,basename="project")
router.register('projectMembers', views.ProjectMembersViewSet,basename="projectMembers")

urlpatterns = [
              ] + router.urls
