from django.db import models
from constructions.models import Project
from django.core.exceptions import ValidationError

# Create your models here.

def validate_file_size(value):
    # Limit the file size to 100MB (100 * 1024 * 1024 bytes)
    max_size = 10 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError('File size cannot exceed 10MB.')

class AdditionalModification(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    file = models.FileField(upload_to ='additional_modification_files',null=True, blank=True,validators=[validate_file_size])

    comment = models.CharField(max_length=255)