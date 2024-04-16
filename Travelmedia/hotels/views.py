from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Permission
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from Travelmedia.hotels.forms import AddHotelForm, EditHotelForm, HotelPhotoForm

from Travelmedia.hotels.models import Hotel, HotelPhoto
from django.contrib import messages
import logging

class AddHotelView(LoginRequiredMixin,views.CreateView):
    form_class = AddHotelForm
    template_name = 'hotels/add_hotel.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

def my_view(request):
    if request.user.is_authenticated:
        # User is authenticated, proceed with the view logic
         return HttpResponse('Welcome, {}'.format(request.user.email))
    else:
        # User is not authenticated, handle accordingly
        return HttpResponseForbidden('You are not logged in.')


class HotelDescription(views.DetailView):
    queryset = Hotel.objects.all() \
                .prefetch_related('photos__likes') \
                .prefetch_related('photos__comments')

    template_name = 'hotels/hotel_description.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel = self.get_object()
        photos = hotel.photos.all()

        context['page_obj'] = photos
        return context

class HotelEditView(LoginRequiredMixin,UserPassesTestMixin,views.UpdateView):
    model = Hotel
    form_class = EditHotelForm
    template_name = "hotels/hotel_edit.html"

    def get_success_url(self):
        return reverse("hotel description", kwargs={
            "pk": self.object.pk,
        })

    def form_valid(self, form):
        # Save the form data to update the hotel object
        self.object = form.save()
        return super().form_valid(form)

    def test_func(self):
        hotel = self.get_object()
        return self.request.user == hotel.owner


class HotelDeleteView(LoginRequiredMixin, UserPassesTestMixin,views.DeleteView):
    model = Hotel
    template_name = "hotels/hotel_delete.html"
    success_url = reverse_lazy('index')

    def test_func(self):
        hotel = self.get_object()
        return self.request.user == hotel.owner

@login_required
def add_photo(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)  # Retrieve the hotel instance using the pk

    # Check if the current user is the owner of the hotel
    if request.user != hotel.owner:
        messages.error(request, "You don't have permission to add a photo to this hotel.")
        return redirect('hotel description', pk=pk)  # Redirect to the hotel description page

    if request.method == 'POST':
        form = HotelPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            hotel_photo = form.save(commit=False)
            hotel_photo.hotel = hotel  # Assign the hotel instance
            hotel_photo.uploaded_by = request.user
            hotel_photo.save()
            hotel.photos.add(hotel_photo)
            return redirect('hotel description', pk=pk)  # Redirect back to the hotel description page
    else:
        form = HotelPhotoForm()


    return render(request, 'hotels/hotel_description.html',
                  {'form': form, 'hotel': hotel})


@staff_member_required
def delete_photo(request, pk):
    hotel_photo = get_object_or_404(HotelPhoto, pk=pk)

    if request.method == 'POST':
        hotel_photo.delete()
        return redirect('hotel description', pk=hotel_photo.hotel.pk)

def verify_permission_assignment(request):
    # Replace 'username_of_the_user' with the username of the user you want to check
    email = 'lora.ivanova2@a1.bg'
    try:
        User = get_user_model()

        user = User.objects.get(email=email)

        can_upload_photo_permission = Permission.objects.get(codename='can_upload_photo')

        has_permission = user.user_permissions.filter(id=can_upload_photo_permission.id).exists()

        return HttpResponse(f"User '{email}' has 'can_upload_photo' permission: {has_permission}")

    except User.DoesNotExist:

        return HttpResponse("User does not exist")

    except Permission.DoesNotExist:

        return HttpResponse("Permission does not exist")