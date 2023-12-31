from django.db import models
from constructions.models import Project
from django.core.exceptions import ValidationError
from members.models import User


# Create your models here.

def validate_file_size(value):
    # Limit the file size to 100MB (100 * 1024 * 1024 bytes)
    max_size = 10 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError('File size cannot exceed 10MB.')


class Approval(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=False)
    file = models.FileField(upload_to='approval_files', null=True, blank=True,
                            validators=[validate_file_size])
    note = models.TextField()
    date_created = models.DateField(auto_created=True, auto_now=True)

    def __str__(self):
        return str(self.project) + " | " + str(self.title)


class ApprovalComment(models.Model):
    approval = models.ForeignKey(Approval, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    file = models.FileField(upload_to='approval_comment_files', null=True, blank=True,
                            validators=[validate_file_size])

    date_created = models.DateField(auto_created=True, auto_now=True)

    def __str__(self):
        return str(self.approval) + " | " + str(self.comment)
