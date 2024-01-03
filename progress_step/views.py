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

    def create(self, request, *args, **kwargs):
        user = self.request.user
        parent = self.request.data.get('parent')
        project_id = self.request.data.get('project')

        if not project_id or not project_id.isdigit():
            return Response("project_id cant be none or letters ", status=status.HTTP_400_BAD_REQUEST)
        print("parent"*3,parent)


        project = get_object_or_404(Project, id=project_id)
        main_project_steps_count = ProgressStep.objects.filter(project_id=project_id,parent=None).count()
        print(main_project_steps_count)
        if parent:
            sub_steps_count = ProgressStep.objects.filter(parent=parent).count()
            main_project_steps_count = ProgressStep.objects.filter(project_id=project_id,parent=parent).count()


        print(project)
        print(project_id)

        if project.project_owner != user:
            return Response("Not the owner of the project ", status=status.HTTP_400_BAD_REQUEST)

        # if not parent and project.project_owner != user:
        #     return Response("Cant Create main Step", status=status.HTTP_400_BAD_REQUEST)

        if not parent and main_project_steps_count > 10:
            return Response("The main steps exceeded 10", status=status.HTTP_400_BAD_REQUEST)

        if parent and sub_steps_count > 10:
            return Response("The sub steps exceeded 10", status=status.HTTP_400_BAD_REQUEST)

        if parent:
            # If the user sent a parent ID, get the last order of child steps under that parent
            last_order = ProgressStep.objects.filter(parent=parent).aggregate(Max('order'))['order__max']
            order = last_order + 1 if last_order is not None else 0
        else:
            # If no parent ID sent, get the last order of main steps in the project
            last_order = ProgressStep.objects.filter(project_id=project_id, parent__isnull=True).aggregate(Max('order'))[
                'order__max']
            order = last_order + 1 if last_order is not None else 0

        print(order)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user,order=order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
