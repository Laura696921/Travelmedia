from django.urls import path, include

from Travelmedia.common.views import add_comment_to_photo, add_like_to_photo, remove_like_from_photo, delete_comment
from Travelmedia.hotels.views import AddHotelView, \
    HotelDescription, HotelEditView, HotelDeleteView, add_photo, \
    delete_photo

urlpatterns = (
    path('add-hotel/', AddHotelView.as_view(), name='add hotel'),
    path('hotel/<int:pk>/', include([
            path('', HotelDescription.as_view(), name='hotel description'),
            path('add_photo/', add_photo, name='add photo'),
            path('delete_photo/', delete_photo, name='delete photo'),
            path('add_comment_to_photo/',add_comment_to_photo, name= 'add_comment_to_photo'),
            path('add_like_to_photo/', add_like_to_photo, name='add_like_to_photo'),
            path('remove_like_from_photo/', remove_like_from_photo, name='remove_like_from_photo'),

            path('edit/', HotelEditView.as_view(), name = 'edit hotel'),
            path('delete/', HotelDeleteView.as_view(), name = 'delete hotel'),

    ]))


)
