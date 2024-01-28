# projects/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from notifcations.models import Notification
from .models import ProjectMember

@receiver(post_save, sender=ProjectMember)
def project_member_added(sender, instance, created, **kwargs):
    if created:
        # Customize the message based on your needs
        message = f"You have joined the project: {instance.project.title}"
        type = "project_member"
        # Create a notification for the user who joined the project
        Notification.objects.create(user=instance.member, message=message,type=type,
                                    extra_data={"project_id": instance.project.id,
                                                })
