from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, VerifiedPhone
from .serializers import ProfileSerializer, MyProfileSerializer, \
    CustomTokenObtainPairSerializer
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.contrib.auth.signals import user_logged_out
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from djoser.utils import decode_uid
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
import random
import string
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext as _

# Create your views here.

# Function to generate a random OTP
def generate_otp(length=6):
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def error_404_view(request, exception):
    return render(request, '404.html')


class ProfileViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):

        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['GET', 'PUT'])
    def me(self, request):

        profile = get_object_or_404(User, id=request.user.id)

        if request.method == "GET":
            serializer = MyProfileSerializer(profile)

            return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response(serializer.data)

        elif request.method == "PUT":
            serializer = ProfileSerializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

            # return Response(serializer.data)

    @action(detail=True, methods=['GET'])  # Change 'POST' to 'GET' and detail to True
    def GetProfileByUserId(self, request, pk=None):  # Use 'pk' to capture the user_id from the URL
        profile = get_object_or_404(User, id=pk)

        serializer = MyProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if not request.user.is_superuser:
            raise PermissionDenied("Permission denied. Only admin users can delete profiles.")

            # return JsonResponse(response_data, status.HTTP_403_FORBIDDEN)

            # return Response({'detail': 'Permission denied. Only admin users can delete profiles.'},
            #                 status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Remove the authenticated user's ID from the request and flush their session
    data.
    """
    # Dispatch the signal before the user is logged out so the receivers have a
    # chance to find out *who* logged out.

    user = getattr(request, "user", None)
    if not getattr(user, "is_authenticated", True):
        user = None

    user_logged_out.send(sender=user.__class__, request=request, user=user)
    request.session.flush()
    if hasattr(request, "user"):
        from django.contrib.auth.models import AnonymousUser
        print(request)
        # request.user.auth_token.delete()
        request.user = AnonymousUser()

    return JsonResponse({"message": "You have logged out"}, status=status.HTTP_200_OK)
    # return Response("logged out")


class UserActivationView(APIView):
    def get(self, request, uid, token):
        try:
            # Decode the uid to get the user object
            user_id = decode_uid(uid)
            user = get_object_or_404(User, id=user_id)
            # Check if the token is valid
            if user.is_active == False:
                # Activate the user's account
                user.is_active = True
                user.save()
                return JsonResponse({"message": "Your account has been activated"}, status=status.HTTP_200_OK)
            else:
                return JsonResponse({"message": "Already activated"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error activating account: {e}")
            return JsonResponse({"message": "Error activating your account"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@csrf_exempt
# class UserResetPassword(APIView):
def UserResetPassword(request, uid, token):
    protocol = 'https://' if request.is_secure() else 'http://'
    web_url = protocol + request.get_host()
    post_url = web_url + "/auth/users/reset_password_confirm/"

    new_password = request.data.get('new_password')
    print(new_password)
    post_data = {'uid': uid, 'token': token, 'new_password': new_password}
    result = requests.post(post_url, data=post_data)
    print(result)
    if result.status_code == 200:
        return Response("Account password change", status=status.HTTP_200_OK)
    else:
        return Response("Invalid token or link expired", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def IsVerified(request):
    requested_phone_number = request.data.get("phone_number")
    print(requested_phone_number)
    phone_in_table = get_object_or_404(VerifiedPhone, phone_number=requested_phone_number)
    print(phone_in_table)
    if phone_in_table.is_verified:
        return Response("This phone number is verified", status=status.HTTP_200_OK)
    else:
        raise PermissionDenied("This phone number not verified")




@api_view(['POST'])
def PreRegister(request):
    requested_phone_number = request.data.get("phone_number")
    print(requested_phone_number)
    phone_in_table = VerifiedPhone.objects.filter(phone_number=requested_phone_number)
    print(phone_in_table)
    if phone_in_table:
        phone_number = phone_in_table[0]
        if phone_number.is_verified:
            return Response(_("This phone number is verified"), status=status.HTTP_200_OK)
        else:
            otp_code = generate_otp()
            # Store the OTP along with phone number and expiration time (10 minutes from now)
            expiration_time = timezone.now() + timezone.timedelta(minutes=10)

            phone_number.otp = otp_code
            phone_number.expires_at = expiration_time
            phone_number.save()

            print(otp_code)
            # Here, you might send the OTP via SMS or other means
            return Response("OTP has been sent", status=status.HTTP_200_OK)
    else:
        otp_code = generate_otp()
        # Store the OTP along with phone number and expiration time (10 minutes from now)
        expiration_time = timezone.now() + timezone.timedelta(minutes=10)

        VerifiedPhone.objects.create(
            phone_number=requested_phone_number,
            otp=otp_code,
            expires_at=expiration_time
        )
        print(otp_code)
        # Here, you might send the OTP via SMS or other means
        return Response("The account has been created OTP has been sent", status=status.HTTP_200_OK)
@api_view(['POST'])
def SendOTP(request):
    requested_phone_number = request.data.get("phone_number")
    print(requested_phone_number)
    phone_in_table = get_object_or_404(VerifiedPhone,phone_number=requested_phone_number)
    print(phone_in_table)
    if phone_in_table.is_verified:
        return Response("This phone number is verified", status=status.HTTP_200_OK)
    else:
        otp_code = generate_otp()
        # Store the OTP along with phone number and expiration time (10 minutes from now)
        expiration_time = timezone.now() + timezone.timedelta(minutes=10)
        phone_in_table.otp = otp_code
        phone_in_table.expires_at = expiration_time
        phone_in_table.save()

        print(otp_code)
        # Here, you might send the OTP via SMS or other means
        return Response("OTP has been sent", status=status.HTTP_200_OK)



@api_view(['POST'])
def VerifyOTP(request):
    # Retrieve the OTP record associated with the phone number
    requested_phone_number = request.data.get("phone_number")
    otp_entered = request.data.get("otp")

    phone_number = get_object_or_404(VerifiedPhone,phone_number=requested_phone_number)
    print(phone_number)
    if phone_number:
        current_time = timezone.now()
        # Check if the OTP matches and it's not expired
        if phone_number.otp == otp_entered and current_time <= phone_number.expires_at:
            # Perform actions if the OTP is valid and within the time frame
            # For example, grant access, update verification status, etc.
            # Delete the OTP record as it's no longer needed
            phone_number.is_verified = True
            phone_number.save()

            return Response("OTP has been entered is correct", status=status.HTTP_200_OK)
    raise PermissionDenied("OTP has been entered is wrong")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()
