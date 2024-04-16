from django.urls import path

from Travelmedia.common.views import load_more_comments, delete_comment, about_us, \
    search_hotels_in_europe,search_hotels_in_western_europe,search_hotels_in_eastern_europe, \
search_hotels_in_balkans

urlpatterns = [
    path('load-more-comments/', load_more_comments, name='load_more_comments'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete comment'),
    path('about-us', about_us, name='about_us'),
    path('search-europe/', search_hotels_in_europe, name='search hotels in europe'),
    path('search-east/', search_hotels_in_eastern_europe, name='search hotels in east europe'),
    path('search-west/', search_hotels_in_western_europe, name='search hotels in west europe'),
    path('search-balkans/', search_hotels_in_balkans, name='search hotels in balkans'),

]
