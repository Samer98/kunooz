from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField
# Create your models here.

def validate_file_size(value):
    # Limit the file size to 100MB (100 * 1024 * 1024 bytes)
    max_size = 10 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError('File size cannot exceed 10MB.')

class Role(models.Model):
    ROLE_CHOICES= [
        ('Consultant', "Consultant"),
        ("User", "User"),
        ("Worker", "Worker"),
        ("Owner", "Owner"),

    ]
    role = models.CharField(choices=ROLE_CHOICES,max_length=255, null=True, blank=True)

    def __str__(self):
        return self.role
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
    MY_SERVICES_CHOICES = (
                  ('1', '1'),
                  ('item_key2', 'Item title 1.2'),
                  ('item_key3', 'Item title 1.3'),
                  ('item_key4', 'Item title 1.4'),
                  ('item_key5', 'Item title 1.5')
    )
    username = None
    username_validator = None
    # is_verified field
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    second_name = models.CharField(max_length=255, null=True, blank=True)
    # personal_date = models.DateField(
    #     null=True,  # You can set this to True if the field is optional
    #     blank=True,  # You can set this to True if the field can be left empty
    #     help_text="User's personal date"
    # )
    company_name = models.CharField(max_length=255, null=True, blank=True)
    job_name = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.ImageField(upload_to ='profile_picture',null=True, blank=True,validators=[validate_file_size])
    introduction = models.TextField(null=True, blank=True)
    cv = models.FileField(validators=[validate_file_size],null=True,blank=True)
    role = models.ForeignKey(Role,on_delete=models.PROTECT,default=None)
    services = MultiSelectField(choices=MY_SERVICES_CHOICES,max_length=20,default="None")
    Commercial_license = models.FileField(validators=[validate_file_size],null=True,blank=True)

    projects_limits = models.IntegerField(default=0)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone_number)



class VerifiedPhone(models.Model):
    phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=False, blank=False) # Assuming OTP is a 6-digit code, adjust as needed
    expires_at = models.DateTimeField()
    def __str__(self):
        return f"{self.phone_number}"

