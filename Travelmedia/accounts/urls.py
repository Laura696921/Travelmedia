from django.urls import path, include

from Travelmedia.accounts.views import IndexView, LoginView, RegisterView, ProfileDescription, ProfileDeleteView, \
    ProfileEditView, signout_user
from Travelmedia.common.views import  WesternEuropeHotelListView, BalkansHotelListView, \
    EasternEuropeHotelListView, EuropeHotelListView

urlpatterns = (
    path('', IndexView.as_view(), name='index'),
    path('western-europe/', WesternEuropeHotelListView.as_view(), name='western_europe_hotels'),
    path('balkans/', BalkansHotelListView.as_view(), name='balkans_hotels'),
    path('eastern-europe/', EasternEuropeHotelListView.as_view(), name='eastern_europe_hotels'),
    path('europe/', EuropeHotelListView.as_view(), name='europe_hotels'),
    path('login/', LoginView.as_view(), name='login user'),
    path('logout/', signout_user, name='logout user'),
    path('register/', RegisterView.as_view(), name='register_user'),
    path('profile/<int:pk>/', include([
        path("", ProfileDescription.as_view(), name="details profile"),
        path("edit/", ProfileEditView.as_view(), name="edit profile"),
        path('delete/', ProfileDeleteView.as_view(), name='profile-delete'),
    ])),



)