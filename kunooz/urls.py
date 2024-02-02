"""
URL configuration for kunooz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from members.views import CustomTokenObtainPairView
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='custom_token_create'),

    path('auth/', include('djoser.urls')),
    path("auth/", include("djoser.social.urls")),
    path('auth/', include('djoser.urls.jwt')),
    path('members/', include('members.urls')),
    path('constructions/', include('constructions.urls')),
    path('additional_modification/', include('additional_modification.urls')),
    path('progress_step/', include('progress_step.urls')),
    path('approval/', include('approval.urls')),
    path('report/', include('report.urls')),
    path('note/', include('note.urls')),
    path('notifcations/', include('notifcations.urls')),
    path('pricing_tender/', include('pricing_tender.urls')),

] + static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)
