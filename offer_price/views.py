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
from .models import OfferPrice, OfferPriceComment
from constructions.models import Project, ProjectMember
from members.models import User
from .serializers import OfferPriceSerializers, OfferPriceCommentSerializers
from django.db.models import Q
from rest_framework.response import Response
from django.utils.translation import gettext as _
from kunooz.permissions import IsConsultant, IsWorker, IsOwner, IsConsultant_Worker_Owner
from django.utils.dateparse import parse_date


# Create your views here.


class OfferPriceViewSet(ModelViewSet):
    queryset = OfferPrice.objects.all()
    serializer_class = OfferPriceSerializers
    permission_classes = [IsConsultant]

    def get_permissions(self):

        if self.request.method == "GET":
            return [IsConsultant_Worker_Owner()]
        return [IsConsultant()]

    def retrieve(self, request, *args, **kwargs):
        project_id = self.kwargs.get('pk')  # Get project_name from URL
        owner = self.request.user
        project = get_object_or_404(Project, id=project_id)

        name_filter = self.request.query_params.get('title')
        start_date_filter = self.request.query_params.get('start_date')
        end_date_filter = self.request.query_params.get('end_date')

        if project.project_owner != owner:
            raise PermissionDenied("Not the owner of the project")

        records = OfferPrice.objects.filter(project_id=project_id)

        if name_filter:
            records = records.filter(title__icontains=name_filter)

        if start_date_filter and end_date_filter:
            try:
                start_date = parse_date(start_date_filter)
                end_date = parse_date(end_date_filter)
                records = records.filter(date_created__range=[start_date, end_date])
            except (ValueError, TypeError):
                raise PermissionDenied("Invalid date format. Use YYYY-MM-DD")

        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        owner = self.request.user
        project_id = self.request.data.get('project')
        project = get_object_or_404(Project, id=project_id)

        if project.project_owner != owner:
            raise PermissionDenied("Not the owner of the project")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        record = self.get_object()
        user = request.user
        if record.project.project_owner != user:
            raise PermissionDenied(_("You are not the owner of this record"))

        serializer = self.get_serializer(record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        record = self.get_object()
        user = request.user

        print(record)
        if record.project_owner != user:
            raise PermissionDenied(_("You are not the owner of this record"))

        record.delete()


class OfferPriceCommentViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    queryset = OfferPriceComment.objects.all()
    serializer_class = OfferPriceCommentSerializers
    permission_classes = [IsConsultant_Worker_Owner]

    def retrieve(self, request, *args, **kwargs):
        approval_id = self.kwargs.get('pk')  # Get project_name from URL
        user = self.request.user
        offer_price = get_object_or_404(OfferPrice, id=approval_id)
        project_id = offer_price.project_id
        project = get_object_or_404(Project, id=project_id)
        project_member = ProjectMember.objects.filter(project_id=project_id, member=user)

        if not project_member and project.project_owner != user:
            return Response("Not a member of the project", status=status.HTTP_400_BAD_REQUEST)

        records = OfferPriceComment.objects.filter(approval=approval_id)

        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        project_id = self.request.data.get('project')
        project = get_object_or_404(Project, id=project_id)
        project_member = ProjectMember.objects.filter(project_id=project_id, member=user)
        if not project_member and project.project_owner != user:
            return Response("Not a member of the project", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
