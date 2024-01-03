from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import AdditionalModification, AdditionalModificationComment
from constructions.models import Project, ProjectMember
from members.models import User
from .serializers import AdditionalModificationSerializers, AdditionalModificationCommentSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.utils.translation import gettext as _
from kunooz.permissions import IsConsultant, IsWorker, IsOwner, IsConsultant_Worker_Owner
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


class AdditionalModificationViewSet(ModelViewSet):
    queryset =AdditionalModification.objects.all()
    serializer_class = AdditionalModificationSerializers
    permission_classes = [IsConsultant]

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]
        return [IsConsultant()]

    def retrieve(self, request, *args, **kwargs):
        print("Hello")
        project_id = self.kwargs.get('pk')  # Get project_name from URL
        owner = self.request.user
        print("$"*20,project_id)
        project = get_object_or_404(Project, id=project_id)
        print("$"*20,project)

        if project.project_owner != owner:
            return Response("Not the owner of the project", status=status.HTTP_400_BAD_REQUEST)

        records = AdditionalModification.objects.filter(project_id=project_id)

        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

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

    def update(self, request, *args, **kwargs):
        record = self.get_object()
        user = request.user
        print("record")
        if record.project.project_owner != user:
            return Response(_("You are not the owner of this record"), status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        record = self.get_object()
        user = request.user

        print(record)
        if record.project_owner != user:
            return Response(_("You are not the owner of this record"), status=status.HTTP_403_FORBIDDEN)

        record.delete()





class AdditionalModificationCommentViewSet(RetrieveModelMixin,CreateModelMixin,GenericViewSet):
    queryset =AdditionalModificationComment.objects.all()
    serializer_class = AdditionalModificationCommentSerializers
    permission_classes = [IsConsultant_Worker_Owner]

    # def get_permissions(self):
    #
    #     if self.request.method == "GET":
    #         return [AllowAny()]
    #     return self.permission_classes

    def retrieve(self, request, *args, **kwargs):
        print("Hello")
        additional_modification_id = self.kwargs.get('pk')  # Get project_name from URL
        user = self.request.user
        additional_modification = get_object_or_404(AdditionalModification,id=additional_modification_id)
        project_id = additional_modification.project_id
        project = get_object_or_404(Project, id=project_id)
        project_member = ProjectMember.objects.filter(project_id=project_id, member=user)

        if not project_member and project.project_owner != user:
            return Response("Not a member of the project", status=status.HTTP_400_BAD_REQUEST)

        records = AdditionalModificationComment.objects.filter(additional_modification=additional_modification_id)

        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        project_id = self.request.data.get('project')
        project = get_object_or_404(Project, id=project_id)
        project_member = ProjectMember.objects.filter(project_id=project_id,member=user)
        if not project_member and project.project_owner != user :
            return Response("Not a member of the project", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, *args, **kwargs):
    #     record = self.get_object()
    #     user = request.user
    #     print("record")
    #     if record.project.project_owner != user:
    #         return Response(_("You are not the owner of this record"), status=status.HTTP_403_FORBIDDEN)
    #
    #     serializer = self.get_serializer(record, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response(serializer.data)

    # def delete(self, request, *args, **kwargs):
    #     record = self.get_object()
    #     user = request.user
    #
    #     print(record)
    #     if record.project_owner != user:
    #         return Response(_("You are not the owner of this record"), status=status.HTTP_403_FORBIDDEN)
    #
    #     record.delete()


