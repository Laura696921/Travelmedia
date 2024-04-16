from Travelmedia.accounts.models import AccountUser

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver



UserModel = get_user_model()


class Hotel(models.Model):
    EUROPE = 'Europe'
    WESTERN_EUROPE = 'Western Europe'
    BALKANS = 'Balkans'
    EASTERN_EUROPE =  'Eastern Europe'

    VISIT_STATUS_CHOICES = [
        ('I_was_there', 'I was there'),
        ('I_want_to_go', 'I want to go'),
        ('Never_went', 'Never went'),
        ('Wishing_but_broke', 'Wishing but broke'),
    ]

    LOCATION_CHOICES = [
        (EUROPE, 'Europe'),
        (WESTERN_EUROPE, 'Western Europe'),
        (BALKANS, 'Balkans'),
        (EASTERN_EUROPE, 'Eastern Europe'),
    ]
    name = models.CharField(max_length=30, null=False,blank=False,)
    location = models.CharField(max_length=30, null=False, blank=False, choices=LOCATION_CHOICES)
    visit_status = models.CharField(max_length=20, null=False, blank=False, choices=VISIT_STATUS_CHOICES,default='I was there')
    picture = models.URLField(null=False,blank=False,)
    description = models.TextField(null=False,blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True, related_name='added_hotels')




class HotelPhoto(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='hotel_photos/')
    uploaded_by = models.ForeignKey(AccountUser,
                                    on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.hotel.name} - {self.id}'




@receiver(post_migrate)
def upload_photo(sender, **kwargs):
    if sender.name == 'Travelmedia.hotels':
        content_type = ContentType.objects.get_for_model(HotelPhoto)
        permission, _ = Permission.objects.get_or_create(
            codename='can_upload_photo',
            name='Can Upload Photo',
            content_type=content_type,
        )