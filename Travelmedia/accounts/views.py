from django.contrib import messages

from django.shortcuts import render, redirect

from django.urls import reverse_lazy, reverse
from django.views import generic as views
from django.contrib.auth import views as auth_views, login, logout
from django.views.generic import TemplateView

from Travelmedia.accounts.forms import AccountUserCreationForm
from Travelmedia.accounts.models import Profile




class IndexView(TemplateView):
    template_name = 'index.html'

class LoginView(auth_views.LoginView):

    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email or password. Please try again.")
        return super().form_invalid(form)

class RegisterView(views.CreateView):
    form_class = AccountUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):

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

