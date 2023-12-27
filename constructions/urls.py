from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('project', views.ProjectViewSet)

urlpatterns = [
                  path('auth/', include('djoser.urls')),
                  path("auth/", include("djoser.social.urls")),
                  path('auth/', include('djoser.urls.jwt')),
                  path('members/', include('members.urls')),

              ] + router.urls
