from django.apps import AppConfig


class FriendslistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'friendslist'

def ready(self):
        import your_app.signals  # Import signals to ensure they are registered