from django.core.validators import MinValueValidator
from django.db import models
from members.models import User
from constructions.models import Project
# Create your models here.

class ProgressStep(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='parent', null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    order = models.IntegerField(validators=[MinValueValidator(0)])