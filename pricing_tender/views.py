from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import PricingTender, PricingTenderContractor, OfferPrice  # , PricingTinderComment
from constructions.models import Project, ProjectMember
from members.models import User
from .serializers import PricingTenderSerializers, PricingTenderContractorSerializers, \
    OfferPriceSerializers  # ,PricingTinderCommentSerializers,
from django.db.models import Q
from rest_framework.response import Response
from django.utils.translation import gettext as _
from kunooz.permissions import IsConsultant, IsContractor, IsOwner, IsConsultant_Contractor_Owner
from django.utils.dateparse import parse_date
from rest_framework.decorators import action


class PricingTenderViewSet(ModelViewSet):
    queryset = PricingTender.objects.all()
    serializer_class = PricingTenderSerializers
    permission_classes = [IsConsultant]

    def get_permissions(self):

        if self.request.method == "GET":
            return [IsConsultant_Contractor_Owner()]
        return [IsConsultant()]

    def get_queryset(self):
        owner = self.request.user
        queryset = PricingTender.objects.filter(pricing_tender_owner=owner)

        # Additional filters can be applied here if needed
        name_filter = self.request.query_params.get('project_name')
        start_date_filter = self.request.query_params.get('start_date')
        end_date_filter = self.request.query_params.get('end_date')

        if name_filter:
            queryset = queryset.filter(project_name__icontains=name_filter)

        if start_date_filter and end_date_filter:
            try:
                start_date = parse_date(start_date_filter)
                end_date = parse_date(end_date_filter)
                queryset = queryset.filter(date_created__range=[start_date, end_date])
            except (ValueError, TypeError):
                raise PermissionDenied("Invalid date format. Use YYYY-MM-DD")

        return queryset

    def retrieve(self, request, *args, **kwargs):
        pricing_tender_id = self.kwargs.get('pk')
        owner = self.request.user
        pricing_tender = get_object_or_404(PricingTender, id=pricing_tender_id)

        # Check if the user is the owner of the PricingTender
        if pricing_tender.pricing_tender_owner != owner:
            raise PermissionDenied("Not the owner of the project")

        serializer = self.get_serializer(pricing_tender)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        # project_id = self.request.data.get('project')
        # project = get_object_or_404(Project, id=project_id)

        # if project.project_owner != user:
        #     raise PermissionDenied("Not the owner of the project")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(pricing_tender_owner=user)

        users_ids = request.POST.getlist('users', [])
        not_valid_ids = []
        for member in users_ids:
            # print(users_ids)
            try:
                user_to_add = User.objects.get(id=member)

                # Check if the user is not the same as the requester
                if user_to_add == user:
                    print('Cannot add yourself to the project')
                    not_valid_ids.append((user_to_add, 'Cannot add yourself to the project'))

                    continue

                # Check if the user exists and is not a consultant
                if str(user_to_add.role) != 'Contractor':
                    print('user mot Contractor')
                    not_valid_ids.append((user_to_add, 'user need to be Contractor'))

                    continue

                # Check if the user is already a member of the project
                if PricingTenderContractor.objects.filter(pricing_tender=instance, member=user_to_add).exists():
                    not_valid_ids.append((user_to_add, 'User is already a member of the project'))
                    print('User is already a member of the project')
                    continue

                # Create ProjectMember only if the user exists, is a consultant, and not already a member
                PricingTenderContractor.objects.create(pricing_tender=instance, member=user_to_add)
                print('User added')

            except User.DoesNotExist:
                print('User does not exist')
                not_valid_ids.append((user_to_add, 'User does not exist'))

                pass
        # the value maybe it looks like it's not import but dont delete it wont work without it
        serialized_not_valid_users = [
            {'id': user.id, 'first_name': user.first_name, 'phone_number': str(user.phone_number),
             'role': str(user.role)}
            for user, value in not_valid_ids
        ]
        return Response([serializer.data, ("not valid ids", serialized_not_valid_users)],
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        # Check if the user is the owner of the PricingTender
        if instance.pricing_tender_owner != user:
            raise PermissionDenied("Not the owner of the project")

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        users_ids = request.POST.getlist('users', [])
        not_valid_ids = []

        for member in users_ids:
            try:
                user_to_add = User.objects.get(id=member)

                # Check if the user is not the same as the requester
                if user_to_add == user:
                    not_valid_ids.append((user_to_add, 'Cannot add yourself to the project'))
                    continue

                # Check if the user is already a member of the project
                if PricingTenderContractor.objects.filter(pricing_tender=updated_instance, member=user_to_add).exists():
                    not_valid_ids.append((user_to_add, 'User is already a member of the project'))
                    continue

                # Create PricingTenderContractor only if the user exists and not already a member
                PricingTenderContractor.objects.create(pricing_tender=updated_instance, member=user_to_add)

            except User.DoesNotExist:
                not_valid_ids.append((user_to_add, 'User does not exist'))
                pass

        serialized_not_valid_users = [
            {'id': user.id, 'first_name': user.first_name, 'phone_number': str(user.phone_number),
             'role': str(user.role)}
            for user, value in not_valid_ids
        ]

        return Response([serializer.data, ("not valid ids", serialized_not_valid_users)], status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        record = self.get_object()
        user = request.user

        print(record)
        if record.project_owner != user:
            raise PermissionDenied(_("You are not the owner of this record"))

        record.delete()

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        pricing_tender = self.get_object()
        user_id_to_remove = request.data.get('user_id')

        user = self.request.user

        # Check if the user is the owner of the PricingTender
        if pricing_tender.pricing_tender_owner != user:
            raise PermissionDenied("Not the owner of the project")

        try:
            user_to_remove = User.objects.get(id=user_id_to_remove)
        except User.DoesNotExist:
            raise PermissionDenied("User to remove does not exist")

        # Check if the user to remove is a member of the project
        if not PricingTenderContractor.objects.filter(pricing_tender=pricing_tender, member=user_to_remove).exists():
            raise PermissionDenied("User is not a member of the project")

        # Remove the user from PricingTenderContractor
        PricingTenderContractor.objects.filter(pricing_tender=pricing_tender, member=user_to_remove).delete()

        return Response({"message": "User removed successfully"}, status=status.HTTP_200_OK)


# class PricingTinderCommentViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
#     queryset = PricingTinderComment.objects.all()
#     serializer_class = PricingTinderCommentSerializers
#     permission_classes = [IsConsultant_Contractor_Owner]
#
#     def retrieve(self, request, *args, **kwargs):
#         report_id = self.kwargs.get('pk')  # Get project_name from URL
#         user = self.request.user
#         pricing_tender = get_object_or_404(PricingTender, id=report_id)
#         project_id = pricing_tender.project_id
#         project = get_object_or_404(Project, id=project_id)
#         project_member = ProjectMember.objects.filter(project_id=project_id, member=user)
#
#         if not project_member and project.project_owner != user:
#             return Response("Not a member of the project", status=status.HTTP_400_BAD_REQUEST)
#
#         records = PricingTinderComment.objects.filter(report=report_id)
#
#         serializer = self.get_serializer(records, many=True)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         user = self.request.user
#         project_id = self.request.data.get('project')
#         project = get_object_or_404(Project, id=project_id)
#         project_member = ProjectMember.objects.filter(project_id=project_id, member=user)
#         if not project_member and project.project_owner != user:
#             return Response("Not a member of the project", status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=user)
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class OfferPriceViewSet(ModelViewSet):
    queryset = OfferPrice.objects.all()
    serializer_class = OfferPriceSerializers
    permission_classes = [IsConsultant_Contractor_Owner]

    def get_queryset(self):
        owner = self.request.user
        queryset = OfferPrice.objects.filter(owner=owner)

        # Additional filters can be applied here if needed
        name_filter = self.request.query_params.get('title')
        start_date_filter = self.request.query_params.get('start_date')
        end_date_filter = self.request.query_params.get('end_date')

        if name_filter:
            queryset = queryset.filter(title__icontains=name_filter)

        if start_date_filter and end_date_filter:
            try:
                start_date = parse_date(start_date_filter)
                end_date = parse_date(end_date_filter)
                queryset = queryset.filter(date_created__range=[start_date, end_date])
            except (ValueError, TypeError):
                raise PermissionDenied("Invalid date format. Use YYYY-MM-DD")

        return queryset
    def retrieve(self, request, *args, **kwargs):
        pricing_tender_id = self.kwargs.get('pk')  # Get PricingTender ID from URL
        owner = self.request.user
        pricing_tender = get_object_or_404(PricingTender, id=pricing_tender_id)

        offer_price = get_object_or_404(OfferPrice, id=pricing_tender_id)

        if offer_price.owner != owner or pricing_tender.pricing_tender_owner != owner:
            raise PermissionDenied("Not the owner of the offer price nor the owner of price tender")
        serializer = self.get_serializer(offer_price)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        pricing_tender_id = self.request.data.get('pricing_tender')  # Assuming the field is named 'pricing_tender'
        pricing_tender = get_object_or_404(PricingTender, id=pricing_tender_id)
        print(pricing_tender)
        # Check if the user is a member of PricingTenderContractor
        if not PricingTenderContractor.objects.filter(pricing_tender=pricing_tender_id, member=user).exists():
            raise PermissionDenied("Not a member of PricingTenderContractor for this PricingTender")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        record = self.get_object()
        user = request.user
        if record.PricingTender.pricing_tender_owner != user:
            raise PermissionDenied(_("You are not the owner of this record"))

        serializer = self.get_serializer(record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        record = self.get_object()
        user = request.user

        if record.PricingTender.pricing_tender_owner != user:
            raise PermissionDenied(_("You are not the owner of this record"))

        record.delete()
        return Response({"message": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# class OfferPriceCommentViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
#     queryset = OfferPriceComment.objects.all()
#     serializer_class = OfferPriceCommentSerializers
#     permission_classes = [IsConsultant_Contractor_Owner]
#
#     def retrieve(self, request, *args, **kwargs):
#         offer_price_id = self.kwargs.get('pk')  # Get project_name from URL
#         user = self.request.user
#         offer_price = get_object_or_404(OfferPrice, id=offer_price_id)
#         project_id = offer_price.project_id
#         project = get_object_or_404(Project, id=project_id)
#         project_member = ProjectMember.objects.filter(project_id=project_id, member=user)
#
#         if not project_member and project.project_owner != user:
#             return Response("Not a member of the project", status=status.HTTP_400_BAD_REQUEST)
#
#         records = OfferPriceComment.objects.filter(offer_price=offer_price_id)
#
#         serializer = self.get_serializer(records, many=True)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         user = self.request.user
#         project_id = self.request.data.get('project')
#         project = get_object_or_404(Project, id=project_id)
#         project_member = ProjectMember.objects.filter(project_id=project_id, member=user)
#         if not project_member and project.project_owner != user:
#             return Response("Not a member of the project", status=status.HTTP_400_BAD_REQUEST)
#
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=user)
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
