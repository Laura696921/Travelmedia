from django import forms
from django.contrib.auth.forms import UserCreationForm, get_user_model, UserChangeForm


UserModel = get_user_model()

class AccountUserCreationForm(UserCreationForm):
    user = None
    class Meta:
        model = UserModel
        fields = ('email',)


class AccountUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel