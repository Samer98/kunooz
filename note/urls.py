from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('Note', views.NoteViewSet,basename="Note")
router.register('NoteComment', views.NoteCommentViewSet,basename="NoteComment")

urlpatterns = [
              ] + router.urls
