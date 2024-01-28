from rest_framework import viewsets
from .models import Notification
from .serializer import NotificationSerializer
from rest_framework.mixins import  RetrieveModelMixin,  ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
# Create your views here.


class NotificationViewSet( RetrieveModelMixin, ListModelMixin,GenericViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        # Filter notifications for the authenticated user
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Update is_read to True when retrieving a specific notification
        instance.is_read = True
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    @action(detail=False, methods=['GET'])
    def notification_count(self,request):
        count = Notification.objects.filter(user=self.request.user,is_read=False).count()

        return Response(data=count)