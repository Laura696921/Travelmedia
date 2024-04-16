from django import forms
from django.urls import reverse

from Travelmedia.accounts.models import AccountUser
from Travelmedia.hotels.models import Hotel, HotelPhoto


class BaseHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'location', 'visit_status', 'picture', 'description']


class AddHotelForm(BaseHotelForm):
        pass

class HotelPhotoForm(forms.ModelForm):
    photo = forms.ImageField(
        label = 'Image',
        widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
    )
    class Meta:
        model = HotelPhoto
        fields = ['photo']

class EditHotelForm(BaseHotelForm):
   pass

