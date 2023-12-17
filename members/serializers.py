from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User ,VerifiedPhone
from rest_framework.exceptions import PermissionDenied


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # data.update({'id': self.user.id})
        # data.update({'full_name': self.user.full_name})
        # data.update({'is_asker_view': self.user.is_asker_view})
        return data


class UserCreateSerializer(BaseUserCreateSerializer):
    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        if VerifiedPhone.objects.filter(phone_number=phone_number).exists():
            user = super().create(validated_data)
            return user
        else:
            raise PermissionDenied("The phone number not verified")
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','phone_number','password']

class ProfileSerializer(serializers.ModelSerializer):
    is_consultant = serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model = User
        fields = ['id','full_name','personal_date','job_name','introduction',"video",'qualifications','qualifications_img','specializations','specializations_img','services','services_img','is_consultant']

class MyProfileSerializer(serializers.ModelSerializer):
    is_consultant = serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model = User
        fields = ['id','full_name','personal_date','wallet','job_name','introduction',"video",'qualifications','qualifications_img','specializations','specializations_img','services','services_img','is_consultant']

class EditProfileSerializer(serializers.ModelSerializer):
    # is_consultant = serializers.CharField(max_length=255,read_only=True)

    class Meta:
        model = User
        fields = ['id','full_name','personal_date','job_name','introduction',"video",'qualifications','qualifications_img','specializations','specializations_img','services','services_img','is_consultant']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','phone_number']


class UserToAdminSerializer(BaseUserSerializer):
    # full_name = serializers.CharField(max_length=255,read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'full_name', 'email', 'is_superuser','is_staff']
