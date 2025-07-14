from django.apps import AppConfig


class CoursesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Courses_app'

    def ready(self):
        import Courses_app.signals
