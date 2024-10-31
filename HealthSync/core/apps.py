from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # Set the default auto field type
    name = 'core'  # Name of the application

    def ready(self):
        import core.signals  # Import signals when the app is ready