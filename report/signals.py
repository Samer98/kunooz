# projects/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from notifcations.models import Notification
from .models import ReportComment, Report


@receiver(post_save, sender=ReportComment)
def new_report_comment_created(sender, instance, created, **kwargs):
    if created:
        # Customize the message based on your needs
        message = f"تم إنشاء تعليق جديد على التقرير في المشروع {instance.report.project}"
        type = "report_comment"
        # Create a notification for the user who joined the project
        Notification.objects.create(user=instance.user, message=message,type=type,
                                    extra_data = {"project_id":instance.report.project.id,
                                                  "report":instance.report.id,
                                                  "comment_id":instance.id})
        # Notification.set_extra_data({"project_id":instance.additional_modification.project.id, "user_id": new_member.id})



@receiver(post_save, sender=Report)
def new_report_created(sender, instance, created, **kwargs):
    if created:
        # Customize the message based on your needs
        message = f" تم إنشاء تقرير جديد في المشروع {instance.report.project}"
        type = "report"
        project = instance.report.project
        project_owner_id = project.project_owner
        # Create a notification for the user who joined the project
        Notification.objects.create(user=project_owner_id, message=message,type=type,
                                    extra_data = {"project_id":instance.report.project.id,
                                                  "report":str(instance.report)}
                                                  )
