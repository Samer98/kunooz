from rest_framework.decorators import action
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
from kunooz.permissions import IsConsultant, IsContractor, IsOwner, IsConsultant_Contractor_Owner
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Max
from django.db import transaction
from typing import List, Tuple
from .default_step import Arabic_progress_step, English_progress_step


# Create your views here.


class ProgressStepViewSet(ModelViewSet):
    queryset = ProgressStep.objects.all()
    serializer_class = ProgressStepSerializers
    permission_classes = [IsConsultant]

    def get_permissions(self):

        if self.request.method == "GET":
            return [IsConsultant_Contractor_Owner()]
        return [IsConsultant()]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        queryset = self.queryset
        parent = self.request.query_params.get('parent')
        project_id = self.request.query_params.get('project_id')
        project = get_object_or_404(Project, id=project_id)
        project_member = ProjectMember.objects.filter(project_id=project_id, member=user)

        if not project_member and project.project_owner != user:
            raise PermissionDenied("Not a member of the project")
        if not project_id or not project_id.isdigit():
            raise PermissionDenied("project id cant be none or letters")

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
            raise PermissionDenied("project_id cant be none or letters")

        project = get_object_or_404(Project, id=project_id)
        main_project_steps_count = ProgressStep.objects.filter(project_id=project_id, parent=None).count()

        if parent:
            sub_steps_count = ProgressStep.objects.filter(parent=parent).count()
            main_project_steps_count = ProgressStep.objects.filter(project_id=project_id, parent=parent).count()
            last_order = ProgressStep.objects.filter(parent=parent).aggregate(Max('order'))['order__max']
            order = last_order + 1 if last_order is not None else 0
        else:
            last_order = \
                ProgressStep.objects.filter(project_id=project_id, parent__isnull=True).aggregate(Max('order'))[
                    'order__max']
            order = last_order + 1 if last_order is not None else 0

        if project.project_owner != user:
            raise PermissionDenied("Not the owner of the project ")

        if not parent and main_project_steps_count >= steps_limit:
            raise PermissionDenied("The main steps exceeded 10")

        if parent and sub_steps_count >= steps_limit:
            raise PermissionDenied("The sub steps exceeded 10")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, order=order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user
        project = instance.project

        if project.project_owner != user:
            raise PermissionDenied("Not the owner of the project")
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
            raise PermissionDenied("Not the owner of the project")

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

    @action(detail=False, methods=['post'])
    def reorder(self, request):
        ids = request.data.get('ids', [])
        project_id = request.data.get("project_id")

        project = get_object_or_404(Project, id=project_id)
        user = request.user

        # Ensure the user is the owner of the project
        if project.project_owner != user:
            raise PermissionDenied("Not the owner of the project")
        if len(set(ids)) != len(ids):
            raise PermissionDenied("All elements in the list must be  unique.")

        progress_steps = ProgressStep.objects.filter(project_id=project_id, parent=None)
        if len(progress_steps) != len(ids):
            raise PermissionDenied("Length of ids is not right")

        # Create a dictionary mapping ID to the corresponding instance
        id_to_instance = {step.id: step for step in progress_steps}

        # Validate the provided IDs
        for step_id in ids:
            if step_id not in id_to_instance:
                raise PermissionDenied(f"Invalid ProgressStep ID: {step_id}")

        # Reorder the instances based on the provided list of IDs
        with transaction.atomic():
            for index, step_id in enumerate(ids):
                progress_step = id_to_instance[step_id]
                progress_step.order = index
                progress_step.save()

        return Response({"message": f"Project{project_id}, ProgressStep order updated successfully",
                         "new_order": ids}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_standard_steps(self, request):
        project_id = request.data.get("project_id")
        language = request.data.get("language")
        project = get_object_or_404(Project, id=project_id)
        user = request.user

        # Ensure the user is the owner of the project
        if project.project_owner != user:
            raise PermissionDenied("Not the owner of the project")

        existing_steps = ProgressStep.objects.filter(project_id=project_id, parent=None)
        if existing_steps.exists():
            raise PermissionDenied("Cant create these steps cause steps already found")
        # Create a dictionary mapping ID to the corresponding instance
        predefined_steps = Arabic_progress_step if language == "AR" else English_progress_step
        with transaction.atomic():
            main_step_order = 0
            for main_step, sub_steps in predefined_steps.items():
                order = sub_steps.index(sub_steps[0])  # Use the order of the first sub-step
                # Create main step
                main_step_creation = ProgressStep.objects.create(
                    project=project,
                    title=main_step,
                    user=user,
                    order=main_step_order
                )
                main_step_order += 1

                for sub_step_title in sub_steps:
                    # Create sub-steps
                    sub_step_creation = ProgressStep.objects.create(
                        project=project,
                        title=sub_step_title,
                        parent=main_step_creation,
                        user=user,
                        order=order
                    )
                    order += 1
        return Response({"message": f"Standard steps created successfully for Project {project_id}"},
                        status=status.HTTP_200_OK)


class ProgressStepCommentViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    queryset = ProgressStepComment.objects.all()
    serializer_class = ProgressStepCommentSerializers
    permission_classes = [IsConsultant_Contractor_Owner]

    def retrieve(self, request, *args, **kwargs):
        print("Hello")
        sub_step_id = self.kwargs.get('pk')  # Get project_name from URL
        user = self.request.user
        sub_step = get_object_or_404(ProgressStep, id=sub_step_id)
        project_id = sub_step.project_id
        project = get_object_or_404(Project, id=project_id)
        project_member = ProjectMember.objects.filter(project_id=project_id, member=user)

        if not project_member and project.project_owner != user:
            raise PermissionDenied("Not a member of the project")

        records = ProgressStepComment.objects.filter(sub_step=sub_step.id)

        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        # project_id = self.request.data.get('project')
        sub_step_id = self.request.data.get('sub_step')
        sub_step = get_object_or_404(ProgressStep, id=sub_step_id)
        print(sub_step)

        project = get_object_or_404(Project, id=sub_step.project_id)
        print(project)

        project_member = ProjectMember.objects.filter(project_id=project.id, member=user)
        if not project_member and project.project_owner != user:
            raise PermissionDenied("Not a member of the project")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
