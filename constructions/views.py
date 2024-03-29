from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Project, ProjectMember
from members.models import User
from .serializers import ProjectSerializers, ProjectMembersSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.utils.translation import gettext as _
from kunooz.permissions import IsConsultant
from django.db.models import Q
from datetime import datetime
# Create your views here.


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    permission_classes = [IsConsultant]
    filter_backends = [SearchFilter,DjangoFilterBackend]
    search_fields = ['title','start_date','end_date']

    def list(self, request, *args, **kwargs):
        user = self.request.user
        projects = Project.objects.filter(Q(project_owner=user) | Q(projectmember__member=user)).distinct()

        # Get query parameters from URL
        title_query = self.request.query_params.get('title', None)
        start_date_query = self.request.query_params.get('start_date', None)
        end_date_query = self.request.query_params.get('end_date', None)

        if title_query:
            # If there's a title query, filter by it
            projects = projects.filter(title__icontains=title_query)

        if start_date_query and end_date_query:
            # If both start_date and end_date are provided, filter projects by date range
            try:
                start_date = datetime.strptime(start_date_query, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_query, '%Y-%m-%d')
                projects = projects.filter(start_date__gte=start_date, end_date__lte=end_date)
            except ValueError:
                # Handle invalid date format
                return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(projects, many=True)
        response_data = serializer.data

        # Add the count of projects created by the user to the response data
        projects_created_by_user  = Project.objects.filter(project_owner=user).count()
        response_data.append({'projects_created_by_user' : projects_created_by_user})

        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        # projects = Project.objects.filter(project_owner=user)
        project = self.get_object()
        print(project.projectmember_set.filter(member=user).exists())
        if user != project.project_owner and not project.projectmember_set.filter(member=user).exists():
            return Response(_("You don't have permission to view this project"), status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        print(user)

        projects_count = Project.objects.filter(project_owner=user).count()
        if projects_count >= user.projects_limits:
            return Response(_("The user reached the limit of projects"), status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project =serializer.save(project_owner=user)

        users_ids = request.data.get('users',[])
        for member in users_ids:
            try:
                user_to_add = User.objects.get(id=member)

                # Check if the user is not the same as the requester
                if user_to_add == user:
                    print('Cannot add yourself to the project')
                    continue

                # Check if the user exists and is not a consultant
                if user_to_add.role == 'consultant':
                    print('Cant add  a consultant')
                    continue

                # Check if the user is already a member of the project
                if ProjectMember.objects.filter(project=project, member=user_to_add).exists():
                    print('User is already a member of the project')
                    continue

                # Create ProjectMember only if the user exists, is a consultant, and not already a member
                ProjectMember.objects.create(project=project, member=user_to_add)
                print('User added')

            except User.DoesNotExist:
                print('User does not exist')
                pass

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user

        if project.project_owner != user:
            return Response(_("You are not the owner of this project"), status=status.HTTP_403_FORBIDDEN)

        users_ids = request.data.get('users', [])
        for member in users_ids:
            try:
                user_to_add = User.objects.get(id=member)

                # Check if the user is not the same as the requester
                if user_to_add == user:
                    print('Cannot add yourself to the project')
                    continue

                # Check if the user exists and is not a consultant
                if user_to_add.role == 'consultant':
                    print('Cant add  a consultant')
                    continue

                # Check if the user is already a member of the project
                if ProjectMember.objects.filter(project=project, member=user_to_add).exists():
                    print('User is already a member of the project')
                    continue

                # Create ProjectMember only if the user exists, is a consultant, and not already a member
                ProjectMember.objects.create(project=project, member=user_to_add)
                print('User added')

            except User.DoesNotExist:
                print('User does not exist')
                pass


        serializer = self.get_serializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request):
        project_id = self.request.data.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        user = request.user

        if project.project_owner != user:
            return Response(_("You are not the owner of this project"), status=status.HTTP_403_FORBIDDEN)

        project.delete()
        return Response(_(f"Project {project.title} deleted successfully"), status=status.HTTP_204_NO_CONTENT)


class ProjectMembersViewSet(CreateModelMixin, RetrieveModelMixin,DestroyModelMixin, GenericViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMembersSerializers
    permission_classes = [IsConsultant]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        project_id = self.kwargs.get('pk')  # Get project_name from URL
        print(project_id)
        # Getting the Project object using the provided project_name
        project = get_object_or_404(Project, id=project_id)
        print(project)
        if project.project_owner != user:
            return Response(_("You are not the owner of this project"), status=status.HTTP_403_FORBIDDEN)

        # Filtering ProjectMembers by the Project's ID
        project_members = ProjectMember.objects.filter(project_id=project_id)
        users = []
        for member in project_members:
            user_data = {
                "id": member.member.id,
                "first_name": member.member.first_name,
                "phone_number": str(member.member.phone_number)
            }
            users.append(user_data)
        return Response(users, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        member = self.request.data.get('member')
        project_id = self.request.data.get('project')

        # Fetch the project
        project = get_object_or_404(Project, id=project_id)

        # Retrieve the user based on the phone number
        user = get_object_or_404(User, phone_number=member)

        # Check if the requesting user is trying to add themselves
        if request.user == user:
            return Response("Can't add yourself", status=status.HTTP_400_BAD_REQUEST)

        # Check if the user exists in the system
        if not user:
            return Response("User does not exist in the system", status=status.HTTP_400_BAD_REQUEST)

        if ProjectMember.objects.filter(project=project, member=user).exists():
            return Response("the user already exist", status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has the 'Consultant' role
        # Modify this logic as per your actual user model
        if user.role == "Consultant":
            return Response("Can't add a consultant to your project", status=status.HTTP_400_BAD_REQUEST)

        # Create a new ProjectMembers entry
        project_member = ProjectMember.objects.create(project=project, member=user)
        serializer = ProjectMembersSerializers(project_member)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        user_id = self.request.data.get('user_id')
        project_id = self.request.data.get('project_id')

        # Fetch the project
        project = get_object_or_404(Project, id=project_id)

        # Check if the requesting user is the owner of the project
        if project.project_owner != request.user:
            return Response("You are not the owner of this project", status=status.HTTP_403_FORBIDDEN)

        # Retrieve the user based on the phone number
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is a member of the project
        try:
            project_member = ProjectMember.objects.get(project=project, member=user)
        except ProjectMember.DoesNotExist:
            return Response("User is not a member of this project", status=status.HTTP_400_BAD_REQUEST)

        # Delete the project member association
        project_member.delete()

        return Response(f"{user.first_name} {user.phone_number} Member removed from the project", status=status.HTTP_200_OK)