from django.apps import AppConfig


class AccountAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Account_app'

    def ready(self):
        from Account_app import signals
