from django.contrib.auth import get_user_model
from django.db import models

from Travelmedia.hotels.models import Hotel, HotelPhoto

UserModel = get_user_model()


class HotelComment(models.Model):
    MAX_TEXT_LENGTH = 300

    text = models.TextField(
        max_length=MAX_TEXT_LENGTH,
        null=False,
        blank=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,  # Done only on `create`
    )

    modified_at = models.DateTimeField(
        auto_now=True,  # On every save
    )

    hotel_photo = models.ForeignKey(
        HotelPhoto,
        related_name='comments',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(UserModel,
                             on_delete=models.CASCADE)


class HotelLike(models.Model):
    hotel_photo = models.ForeignKey(
        HotelPhoto,
        related_name='likes',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(UserModel,
                             on_delete=models.CASCADE)