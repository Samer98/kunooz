# projects/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from notifcations.models import Notification
from .models import AdditionalModificationComment
from django.utils.translation import gettext_lazy as _

@receiver(post_save, sender=AdditionalModificationComment)
def new_additional_modification_comment_created(sender, instance, created, **kwargs):
    if created:
        # Customize the message based on your needs
        message = _(f"New Additional Modification  comment created at project {instance.additional_modification.project}")
        type = "additional_modification_comment"
        # Create a notification for the user who joined the project
        Notification.objects.create(user=instance.user, message=message,type=type,
                                    extra_data = {"project_id":instance.additional_modification.project.id,
                                                  "additional_modification":str(instance.additional_modification),
                                                  "comment_id":instance.id})
        # Notification.set_extra_data({"project_id":instance.additional_modification.project.id, "user_id": new_member.id})