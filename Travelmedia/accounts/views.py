from django.contrib.auth.mixins import AccessMixin
from django.db.models import Avg, Case, When, IntegerField
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, logout
from django.views.generic import TemplateView

from Travelmedia.accounts.forms import AccountUserCreationForm
from Travelmedia.accounts.models import AccountUser, Profile
from Travelmedia.hotels.models import Hotel


class OwnerRequiredMixin(AccessMixin):
    """Verify that the current user has this profile."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs.get('pk', None):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['europe_hotels'] = Hotel.objects.filter(location='Europe')
        context['western_europe_hotels'] = Hotel.objects.filter(location='Western Europe')
        context['eastern_europe_hotels'] = Hotel.objects.filter(location='Eastern Europe')
        context['balkans_hotels'] = Hotel.objects.filter(location='Balkans')
        return context
    @property
    def hotel_name_pattern(self):
        return self.request.GET.get("hotel_name_pattern", None)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["hotel_name_pattern"] = self.hotel_name_pattern or ""
        return context



    def filter_by_hotel_name_pattern(self, queryset):
        hotel_name_pattern = self.hotel_name_pattern

        filter_query = {}

        if hotel_name_pattern:
            filter_query['hotels__name__icontains'] = hotel_name_pattern

        return queryset.filter(**filter_query)

    def annotate_average_visit_status(self, queryset):
        queryset = queryset.annotate(
            avg_visit_status=Avg(
                Case(
                    When(visit_status='I_was_there', then=4),
                    When(visit_status='I_want_to_go', then=3),
                    When(visit_status='Never_went', then=2),
                    When(visit_status='Wishing_but_broke', then=1),
                    output_field=IntegerField(),
                )
            )
        )
        return queryset

    def sort_by_average_visit_status(self, queryset):
        queryset = queryset.order_by('-avg_visit_status')
        return queryset
class LoginView(auth_views.LoginView):

    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

class RegisterView(views.CreateView):
    form_class = AccountUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # `form_valid` will call `save`
        result = super().form_valid(form)

        login(self.request, form.instance)

        return result

def signout_user(request):
    logout(request)
    return redirect('index')


class ProfileDescription(views.DetailView):
    queryset = Profile.objects \
        .prefetch_related("user") \
        .all()

    template_name = "accounts/details_profile.html"


class ProfileEditView(views.UpdateView):
    queryset = Profile.objects.all()
    template_name = 'accounts/edit_profile.html'
    fields = ("first_name", "last_name", "date_of_birth", "profile_picture")

    def get_success_url(self):
        return reverse("details profile", kwargs={
            "pk": self.object.pk,
        })

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)

        form.fields["date_of_birth"].widget.attrs["type"] = "date"
        form.fields["date_of_birth"].label = "Birthday"
        return form


class ProfileDeleteView(views.DeleteView):
    queryset = Profile.objects.all()
    template_name = "accounts/delete_profile.html"
