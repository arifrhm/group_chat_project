# chat/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Room


class RoomCreationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class LoginForm(AuthenticationForm):
    # Add any additional fields or customization if needed
    class Meta:
        model = User
        fields = ['username', 'password']


class StyledUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].\
                widget.\
                attrs.\
                update({'class': 'mt-1 p-2 w-full border rounded-md'})

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password1',
                  'password2',
                  'first_name',
                  'last_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if the username is already in use
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already in use.')
        return username


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password1',
                  'password2',
                  'first_name',
                  'last_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        # Add custom email validation logic, e.g., check if the email is unique
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        # Check if the username is already in use
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already in use.')
        return username


class RoomRenameForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super(RoomRenameForm, self).__init__(*args, **kwargs)
        # Add additional customization if needed
        self.fields['name'].label = 'New Room Name'
        self.fields['name'].widget.\
            attrs.update({'class': 'form-control'})
