from django.db import models
from .locations import CITY_CHOICES
from members.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Project(models.Model):
    OUTER_DESIGN_CHOICES = (
        ('Residential', _('Residential')),
        ('Commercial', _('Commercial')),
        ('Industrial', _('Industrial')),  # Corrected capitalization
        ('General', _('General')),
        ('Farms', _('Farms'))
    )

    STATUS_CHOICES = (
        ('On Going', _('On Going')),  # Corrected spacing
        ('Completed', _('Completed')),
        ('Canceled', _('Canceled')),
    )
    title = models.CharField(max_length=255, null=False, blank=False)
    project_owner = models.ForeignKey(User, on_delete=models.PROTECT)
    project_number = models.PositiveIntegerField(null=False, blank=False)
    style = models.CharField(max_length=255, null=False, blank=False)
    room_number = models.IntegerField(default=0)
    space = models.IntegerField(default=0)
    # location = models.CharField(choices=CITY_CHOICES, max_length=255, default="Cairo")
    location = models.CharField( max_length=255)
    outer_design = models.CharField(choices=OUTER_DESIGN_CHOICES, max_length=255, default="ٌResidential")
    total_budget = models.PositiveIntegerField(null=False, blank=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    status = models.CharField(choices=STATUS_CHOICES, max_length=255, default="On Going")
    creation_date = models.DateTimeField(auto_now_add=True)  # Add creation date field
    def __str__(self):
        return str(self.title) + " | " + str(self.project_owner.first_name)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project) +" | "+ str(self.member.first_name)
