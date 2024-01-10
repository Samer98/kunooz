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

class PricingTender(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255,null=False,blank=False)
    planing = models.FileField(upload_to='PricingTender_files/planing', null=True, blank=True,
                            validators=[validate_file_size])
    three_d = models.FileField(upload_to='PricingTender_files/three_d', null=True, blank=True,
                            validators=[validate_file_size])
    quantities_and_specifications = models.FileField(upload_to='PricingTender_files/quantities_and_specifications', null=True, blank=True,
                            validators=[validate_file_size])
    other_files = models.FileField(upload_to='PricingTender_files/other_files', null=True, blank=True,
                            validators=[validate_file_size])


    def __str__(self):
        return str(self.project_name) + " | " + str(self.project)

class PricingTenderContractor(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    contractor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project) +" | "+ str(self.contractor.first_name)


class PricingTinderComment(models.Model):
    pricing_tender = models.ForeignKey(PricingTender , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    file = models.FileField(upload_to='offer_price_comment_files', null=True, blank=True,
                            validators=[validate_file_size])

    date_created = models.DateField(auto_created=True, auto_now=True)

    def __str__(self):
        return str(self.pricing_tender) + " | " + str(self.comment)