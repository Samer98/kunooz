from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import ProgressStep, ProgressStepComment
from constructions.models import Project, ProjectMember
from members.models import User
from .serializers import ProgressStepSerializers, ProgressStepCommentSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.utils.translation import gettext as _
from kunooz.permissions import IsConsultant, IsWorker, IsOwner, IsConsultant_Worker_Owner
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Max


# Create your views here.


class ProgressStepViewSet(ModelViewSet):
    queryset = ProgressStep.objects.all()
    serializer_class = ProgressStepSerializers
    permission_classes = [IsConsultant]

    def get_permissions(self):

        if self.request.method == "GET":
            return [IsConsultant_Worker_Owner()]
        return [IsConsultant()]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        parent = self.request.query_params.get('parent')
        project_id = self.request.query_params.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        project_member = ProjectMember.objects.filter(project_id=project_id, member=user)

        if not project_member and project.project_owner != user:
            return Response("Not a member of the project", status=status.HTTP_400_BAD_REQUEST)

        if not project_id or not project_id.isdigit():
            return Response("project id cant be none or letters", status=status.HTTP_400_BAD_REQUEST)

        queryset = queryset.filter(project_id=project_id)

        if parent:
            queryset = queryset.filter(parent=parent)
        else:
            queryset = queryset.filter(parent=None)

        self.queryset = queryset
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        steps_limit = 10
        user = self.request.user
        parent = self.request.data.get('parent')
        project_id = self.request.data.get('project')

        if not project_id or not project_id.isdigit():
            return Response("project_id cant be none or letters ", status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(Project, id=project_id)
        main_project_steps_count = ProgressStep.objects.filter(project_id=project_id, parent=None).count()

        if parent:
            sub_steps_count = ProgressStep.objects.filter(parent=parent).count()
            main_project_steps_count = ProgressStep.objects.filter(project_id=project_id, parent=parent).count()
            last_order = ProgressStep.objects.filter(parent=parent).aggregate(Max('order'))['order__max']
            order = last_order + 1 if last_order is not None else 0
        else:
            last_order = ProgressStep.objects.filter(project_id=project_id, parent__isnull=True).aggregate(Max('order'))[
                    'order__max']
            order = last_order + 1 if last_order is not None else 0

        if project.project_owner != user:
            return Response("Not the owner of the project ", status=status.HTTP_400_BAD_REQUEST)

        if not parent and main_project_steps_count >= steps_limit:
            return Response("The main steps exceeded 10", status=status.HTTP_400_BAD_REQUEST)

        if parent and sub_steps_count >= steps_limit:
            return Response("The sub steps exceeded 10", status=status.HTTP_400_BAD_REQUEST)


        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, order=order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        project = instance.project

        if project.project_owner != user:
            return Response("Not the owner of the project", status=status.HTTP_400_BAD_REQUEST)

        # Implement additional conditions if needed before deletion

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        project = instance.project
        # print(instance)
        # print(instance.project)
        # return Response("hey")

        if project.project_owner != user:
            return Response("Not the owner of the project", status=status.HTTP_400_BAD_REQUEST)

        is_finished = request.data.get('is_finished', None)

        if is_finished is not None:
            instance.is_finished = is_finished
            instance.save()

        if instance.parent:
            parent = instance.parent
            total_children = ProgressStep.objects.filter(parent=parent).count()
            finished_children = ProgressStep.objects.filter(parent=parent, is_finished=True).count()
            print(parent)
            print(total_children)
            print(finished_children)
            if total_children == finished_children:
                # Update the parent step as finished
                parent.is_finished = True
                parent.save()
            else:
                # Update the parent step as not finished
                parent.is_finished = False
                parent.save()


        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)