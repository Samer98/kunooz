from django.apps import AppConfig


class AdditionalModificationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'additional_modification'

    def ready(self):
        import additional_modification.signals