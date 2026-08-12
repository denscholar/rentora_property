from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from core.cloudinary_config import (
            configure_cloudinary,
        )

        configure_cloudinary()
