from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User ,VerifiedPhone
from rest_framework.exceptions import PermissionDenied


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        data.update({'id': self.user.id})
        data.update({'first_name': self.user.first_name})
        data.update({'second_name': self.user.second_name})
        data.update({'role': str(self.user.role)})
        data.update({'profile_picture': str(self.user.profile_picture.url if self.user.profile_picture else None)})
        data.update({'company_name': self.user.company_name})

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
        fields = ['id','phone_number','password','first_name','second_name',
                  'role','company_name','services','Commercial_license']

class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()
    class Meta:
        model = User
        fields = ['id','first_name','second_name','phone_number',
                  'job_name','introduction',"profile_picture",'cv','role','services','Commercial_license']

class MyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','second_name','phone_number',
                  'job_name','job_name','introduction',"profile_picture",'cv','role','services','Commercial_license']

class EditProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','first_name','second_name',
                  'job_name','introduction',"profile_picture",'cv','services','Commercial_license']

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','phone_number']
