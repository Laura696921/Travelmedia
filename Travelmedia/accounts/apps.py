from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "Travelmedia.accounts"

    def ready(self):
        from Travelmedia.accounts.models import Profile
        from Travelmedia.hotels.models import HotelPhoto
        import Travelmedia.accounts.signals