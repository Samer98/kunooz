from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Project
from .serializers import ProjectSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response


# Create your views here.


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        projects = Project.objects.filter(project_owner=user)
        # print(projects)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        projects_count = Project.objects.filter(project_owner=user).count()
        print(projects_count)
        print(user.projects_limits)
        if projects_count  >= user.projects_limits :
           return Response("The user reached the limit of projects", status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project_owner=user)

        # serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
