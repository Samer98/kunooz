from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a User with the given phone_number and password."""
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password=None, **extra_fields):
        """Create and save a SuperUser with the given phone_number and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username = None
    username_validator = None
    # is_verified field
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    second_name = models.CharField(max_length=255, null=True, blank=True)
    personal_date = models.DateField(
        null=True,  # You can set this to True if the field is optional
        blank=True,  # You can set this to True if the field can be left empty
        help_text="User's personal date"
    )

    company_name = models.CharField(max_length=255, null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    # video = models.FileField(upload_to='consultant_videos_uploaded', null=True, blank=True,
    #                          validators=[
    #                              FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    # qualifications = models.TextField(null=True, blank=True)
    # qualifications_img = models.ImageField(upload_to='qualifications_images_uploaded', null=True, blank=True)
    # specializations = models.TextField(null=True, blank=True)
    # specializations_img = models.ImageField(upload_to='specializations_images_uploaded', null=True, blank=True)
    # services = models.TextField(null=True, blank=True)
    # services_img = models.ImageField(upload_to='services_images_uploaded', null=True, blank=True)

    # is_consultant = models.BooleanField(default=False)
    # is_asker_view = models.BooleanField(default=True)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)

class Role(models.Model):
    ROLE_CHOICES= [
        ('Consultant', "Consultant"),
        ("User", "User"),
        ("Worker", "Worker"),
    ]
    role = models.CharField(choices=ROLE_CHOICES,max_length=255, null=True, blank=True)


class VerifiedPhone(models.Model):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=False, blank=False) # Assuming OTP is a 6-digit code, adjust as needed
    expires_at = models.DateTimeField()
    def __str__(self):
        return f"{self.phone_number}"

