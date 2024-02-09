# chat/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RoomCreationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class LoginForm(AuthenticationForm):
    # Add any additional fields or customization if needed
    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    # Add any additional fields or customization if needed
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
