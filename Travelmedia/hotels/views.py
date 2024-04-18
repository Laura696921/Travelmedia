from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from Travelmedia.hotels.forms import AddHotelForm, EditHotelForm, HotelPhotoForm
from Travelmedia.hotels.models import Hotel, HotelPhoto

class AddHotelView(LoginRequiredMixin,views.CreateView):
    form_class = AddHotelForm
    template_name = 'hotels/add_hotel.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


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
        self.object = form.save()
        return super().form_valid(form)




class HotelDeleteView(LoginRequiredMixin, UserPassesTestMixin,views.DeleteView):
    model = Hotel
    template_name = "hotels/hotel_delete.html"
    success_url = reverse_lazy('index')

    def test_func(self):
        hotel = self.get_object()
        return self.request.user == hotel.owner

@login_required
def add_photo(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)



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

