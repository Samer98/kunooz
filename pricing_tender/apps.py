from django.apps import AppConfig


class PricingTenderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pricing_tender'


    def ready(self):
        import pricing_tender.signals