from django.core.validators import MinValueValidator
from django.db import models
from members.models import User
from constructions.models import Project
from django.core.exceptions import ValidationError

# Create your models here.


def validate_file_size(value):
    # Limit the file size to 100MB (100 * 1024 * 1024 bytes)
    max_size = 10 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError('File size cannot exceed 10MB.')

class ProgressStep(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='child_steps', null=True)
    title = models.CharField(max_length=255,null=False,blank=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    order = models.IntegerField(validators=[MinValueValidator(0)])
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " | " + str(self.project) + " | " + str(self.project)

class ProgressStepComment(models.Model):
    sub_step = models.ForeignKey(ProgressStep, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    file = models.FileField(upload_to='additional_modification_comment_files', null=True, blank=True,
                            validators=[validate_file_size])

    date_created = models.DateField(auto_created=True, auto_now=True)

    def __str__(self):
        return str(self.sub_step) + " | " + str(self.comment)