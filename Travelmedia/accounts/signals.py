from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from Travelmedia.accounts.models import Profile, AccountUser

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def user_created(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
