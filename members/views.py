from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import PermissionDenied
from django.utils.translation import gettext as _
from django.contrib.auth.signals import user_logged_out
from django.shortcuts import get_object_or_404
from .models import User, VerifiedPhone
from .serializers import ProfileSerializer, MyProfileSerializer, \
    CustomTokenObtainPairSerializer, EditProfileSerializer
import random
import string
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from kunooz.settings import account_sid, auth_token, verify_sid, verified_number
from twilio.rest import Client


client = Client(account_sid, auth_token)

def send_sms(mobile, OTP_Code):
    # print(account_sid)
    # print(auth_token)
    # print(client.auth,client.account_sid)
    message = client.messages.create(
        messaging_service_sid='MG72ae018b22ca44e1e0715768ca417e06',
        body=f'OTP IS {OTP_Code}',
        to=mobile)
    print(message.status)

# Create your views here.

def is_valid_phone_number(phone_number):
    return carrier._is_mobile(number_type(phonenumbers.parse(phone_number)))

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
    filter_backends = [SearchFilter]
    search_fields = ['phone_number','first_name','last_name']

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
            serializer = EditProfileSerializer(profile, data=request.data)
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


@api_view(['POST'])
@csrf_exempt
def password_reset_phone(request):
    phone_number = request.data.get('phone_number')
    otp_entered = request.data.get('otp')
    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')
    # Retrieve the OTP record associated with the phone number

    if is_valid_phone_number(phone_number) == False:
        raise PermissionDenied("The phone number is not correct")

    phone_record = get_object_or_404(VerifiedPhone, phone_number=phone_number)

    # Check if the OTP matches and it's not expired
    if new_password != confirm_password:
        raise PermissionDenied("password doesnt match")

    current_time = timezone.now()
    if phone_record.otp == otp_entered and current_time <= phone_record.expires_at:
        # Assume you prompt the user to enter a new password
        # Set the new password for the user
        user = get_object_or_404(User, phone_number=phone_number)
        user.set_password(new_password)
        user.save()

        # Optionally, update the OTP record or mark it as used
        phone_record.is_verified = True
        phone_record.save()

        return Response("Password reset successful.", status=status.HTTP_200_OK)
    else:
        return Response("Invalid OTP or OTP expired for password reset.", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def IsVerified(request):
    requested_phone_number = request.data.get("phone_number")
    phone_in_table = get_object_or_404(VerifiedPhone, phone_number=requested_phone_number)
    if phone_in_table.is_verified:
        return Response("This phone number is verified", status=status.HTTP_200_OK)
    else:
        raise PermissionDenied("This phone number not verified")



@api_view(['POST'])
def PreRegister(request):
    requested_phone_number = request.data.get("phone_number")
    phone_in_table = VerifiedPhone.objects.filter(phone_number=requested_phone_number)
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
            send_sms(requested_phone_number, otp_code)
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
        send_sms(requested_phone_number, otp_code)
        # Here, you might send the OTP via SMS or other means
        return Response("The account has been created OTP has been sent", status=status.HTTP_200_OK)


@api_view(['POST'])
def SendOTP(request):
    requested_phone_number = request.data.get("phone_number")

    if is_valid_phone_number(requested_phone_number) == False:
        raise PermissionDenied("The phone number is not correct")

    print(requested_phone_number)
    phone_in_table = get_object_or_404(VerifiedPhone, phone_number=requested_phone_number)
    print(phone_in_table)

    otp_code = generate_otp()
    # Store the OTP along with phone number and expiration time (10 minutes from now)
    expiration_time = timezone.now() + timezone.timedelta(minutes=10)
    phone_in_table.otp = otp_code
    phone_in_table.expires_at = expiration_time
    phone_in_table.save()

    print(otp_code)
    send_sms(requested_phone_number, otp_code)

    # Here, you might send the OTP via SMS or other means
    return Response("OTP has been sent", status=status.HTTP_200_OK)


@api_view(['POST'])
def VerifyOTP(request):
    # Retrieve the OTP record associated with the phone number
    requested_phone_number = request.data.get("phone_number")
    otp_entered = request.data.get("otp")

    phone_number = get_object_or_404(VerifiedPhone, phone_number=requested_phone_number)
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

