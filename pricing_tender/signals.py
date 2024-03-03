# projects/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from notifcations.models import Notification
from .models import PricingTenderContractor,OfferPrice
from django.utils.translation import gettext_lazy as _

@receiver(post_save, sender=PricingTenderContractor)
def pricing_tender_contractor_added(sender, instance, created, **kwargs):
    if created:
        # Customize the message based on your needs
        message = _(f"لقد تمت دعوتك لطرح مناقصه فالمشروع: {instance.pricing_tender.project_name}")
        type = "pricing_tender_contractor"
        # Create a notification for the user who joined the project
        Notification.objects.create(user=instance.member, message=message,type=type,
                                    extra_data={"pricing_tender_id": instance.pricing_tender.id,
                                                })


@receiver(post_save, sender=OfferPrice)
def offer_price_added(sender, instance, created, **kwargs):
    if created:
        # Customize the message based on your needs
        message = _(f"لقد تم اضافه عرض سعر على: {instance.pricing_tender} من قبل {instance.owner}")
        type = "offer_price"
        # Create a notification for the user who joined the project
        Notification.objects.create(user=instance.pricing_tender.pricing_tender_owner, message=message,type=type,
                                    extra_data={"OfferPrice_id": instance.id,
                                                })