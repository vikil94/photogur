from django.forms import CharField, PasswordInput, Form
from photogur.models import Picture
from django import forms


class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['title', 'artist', 'url']
