from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import AdditionalModification
from constructions.models import Project
from members.models import User
from .serializers import AdditionalModificationSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.utils.translation import gettext as _
from kunooz.permissions import IsConsultant
import ast

# Create your views here.


class AdditionalModificationViewSet(ModelViewSet):
    queryset =AdditionalModification.objects.all()
    serializer_class = AdditionalModificationSerializers
    permission_classes = [IsConsultant]

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]
        return [IsConsultant()]

    def create(self, request, *args, **kwargs):
        owner = self.request.user
        project_id = self.request.data.get('project')
        print(project_id)
        project = get_object_or_404(Project, id=project_id)
        print(project)

        if project.project_owner != owner:
            return Response("Not the owner of the project", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
