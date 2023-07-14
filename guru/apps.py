from django.apps import AppConfig


class GuruConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "guru"

    def ready(self):
        from .management import commands
