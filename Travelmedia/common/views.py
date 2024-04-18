from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView

from Travelmedia.common.models import HotelLike, HotelComment
from Travelmedia.hotels.models import HotelPhoto, Hotel


def about_us(request):
    context = {
        'title': 'About Us',
        'text': 'This is some text about us'
    }
    return render(request, 'about.html', context)

def search_hotels_in_eastern_europe(request):
    hotels = Hotel.objects.filter(location='Eastern Europe')

    search_query = request.GET.get('search')
    if search_query:
        hotels = hotels.filter(name__icontains=search_query)

    return render(request, 'eastern_europe_hotels.html', {'eastern_europe_hotels': hotels})

def search_hotels_in_western_europe(request):
    hotels = Hotel.objects.filter(location='Western Europe')
    search_query = request.GET.get('search')
    if search_query:
        hotels = hotels.filter(name__icontains=search_query)

    return render(request, 'western_europe_hotels.html', {'western_europe_hotels': hotels})

def search_hotels_in_balkans(request):
    hotels = Hotel.objects.filter(location='Balkans')

    search_query = request.GET.get('search')
    if search_query:
        hotels = hotels.filter(name__icontains=search_query)

    return render(request, 'balkans_hotels.html', {'balkans_hotels': hotels})


def search_hotels_in_europe(request):
    hotels = Hotel.objects.filter(location='Europe')

    search_query = request.GET.get('search')
    if search_query:
        hotels = hotels.filter(name__icontains=search_query)

    return render(request, 'europe_hotels.html', {'europe_hotels': hotels})

class WesternEuropeHotelListView(ListView):
    template_name = 'western_europe_hotels.html'  # Create a template for displaying Western Europe hotels
    context_object_name = 'western_europe_hotels'

    def get_queryset(self):
        return Hotel.objects.filter(location='Western Europe')

class BalkansHotelListView(ListView):
    template_name = 'balkans_hotels.html'
    context_object_name = 'balkans_hotels'

    def get_queryset(self):
        return Hotel.objects.filter(location='Balkans')


class EasternEuropeHotelListView(ListView):
    template_name = 'eastern_europe_hotels.html' 
    context_object_name = 'eastern_europe_hotels'

    def get_queryset(self):
        return Hotel.objects.filter(location='Eastern Europe')


class EuropeHotelListView(ListView):
    model = Hotel
    template_name = 'europe_hotels.html'  
    context_object_name = 'europe_hotels'

    def get_queryset(self):
        return Hotel.objects.filter(location='Europe')

@login_required
def add_comment_to_photo(request, pk):
    photo = get_object_or_404(HotelPhoto, pk=pk)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            comment = HotelComment.objects.create(
                text=comment_text,
                hotel_photo=photo,
                user=request.user
            )
    return redirect('hotel description', pk=photo.hotel.id)

@staff_member_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(HotelComment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('hotel_description')
@login_required
def load_more_comments(request):
    if request.method == 'GET':
        photo_id = request.GET.get('photo_id')
        offset = int(request.GET.get('offset', 0))

        photo = HotelPhoto.objects.get(pk=photo_id)

        comments = photo.comments.all()[offset:offset+3]

        html_comments = ""
        for comment in comments:
            html_comments += f"<div class='mb-3'><p class='card-text'>{comment.text}</p><p class='card-text'><small class='text-muted'>By: {comment.user.username}</small></p></div>"

        return JsonResponse({'html_comments': html_comments})

    # Handle invalid requests
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def add_like_to_photo(request, pk):
    photo = get_object_or_404(HotelPhoto, pk=pk)

    if request.user.is_authenticated:
        like, created = HotelLike.objects.get_or_create(
            hotel_photo=photo,
            user=request.user
        )

    else:
        return redirect('login user')
    return redirect('hotel description', pk=photo.hotel.id)

@login_required
def remove_like_from_photo(request, pk):
    photo = get_object_or_404(HotelPhoto, pk=pk)
    try:
        like = HotelLike.objects.get(
            hotel_photo=photo,
            user=request.user
        )
        like.delete()
    except HotelLike.DoesNotExist:
        pass
    return redirect('hotel description', pk=photo.hotel.id)
