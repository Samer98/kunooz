from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Project,ProjectMembers
from members.models import User
from .serializers import ProjectSerializers , ProjectMembersSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.utils.translation import gettext as _


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
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        projects_count = Project.objects.filter(project_owner=user).count()
        if projects_count >= user.projects_limits:
            return Response(_("The user reached the limit of projects"), status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project_owner=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user

        if project.project_owner != user:
            return Response(_("You are not the owner of this project"), status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user

        if project.project_owner != user:
            return Response(_("You are not the owner of this project"), status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response(_("Project deleted successfully"), status=status.HTTP_204_NO_CONTENT)
class ProjectMembersViewSet(ModelViewSet):
    queryset = ProjectMembers.objects.all()
    serializer_class = ProjectMembersSerializers
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        project_name = self.kwargs.get('pk')  # Get project_name from URL
        print(project_name)
        # Getting the Project object using the provided project_name
        project = get_object_or_404(Project, id=project_name)

        # Filtering ProjectMembers by the Project's ID
        project_members = ProjectMembers.objects.filter(project_id=project.id)

        if project.project_owner != user:
            return Response(_("You are not the owner of this project"), status=status.HTTP_403_FORBIDDEN)

        users = [member.user.username for member in project_members]
        return Response(users, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user_phone = self.request.data.get('user_phone')
        project_id = self.request.data.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        # Check if the user exists in the system
        if not User.objects.filter(phone_number=user_phone).exists():
            return Response("User does not exist in the system", status=status.HTTP_400_BAD_REQUEST)
        user_phone = User.objects.get(phone_number=user_phone).id
        print(user_phone)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project,user_phone=user_phone)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

