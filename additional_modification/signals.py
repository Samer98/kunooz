# projects/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from notifcations.models import Notification
from .models import AdditionalModificationComment

@receiver(post_save, sender=AdditionalModificationComment)
def new_report_comment_created(sender, instance, created, **kwargs):
    if created:
        # Customize the message based on your needs
        message = {"message":f"New comment created at project {instance.additional_modification.project}","project_id":instance.additional_modification.project.id}
        type = "comment"
        # Create a notification for the user who joined the project
        Notification.objects.create(user=instance.user, message=message,type=type)
