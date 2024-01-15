from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from . import views
from members import views
from django.views.generic import TemplateView

router = routers.DefaultRouter()
router.register('profile', views.ProfileViewSet, basename='profile')

# router.register('user_to_admin', views.UserToAdminViewSet, basename='user_to_admin')


urlpatterns = [
    path('VerifyOTP/', views.VerifyOTP),
    path('SendOTP/', views.SendOTP),
    path('IsVerified/', views.IsVerified),
    path('PreRegister/', views.PreRegister),
    path('password_reset_phone/', views.password_reset_phone, name='password_reset_phone'),
    path('logout/', views.logout, name='logout'),

              ]+ router.urls


