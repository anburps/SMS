from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User
from .models import UserProfile

class UserEditForm(forms.ModelForm):
    """Form for viewing and editing name fields in a User object."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('display_name',)


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'display_name',
                  'is_staff', 'is_active')

    def is_valid(self):
        return super().is_valid()


class MySignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('display_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """docstring for ProfileEditForm."""
    class Meta:
        model = UserProfile
        fields = ['photo']
