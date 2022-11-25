from allauth.socialaccount.forms import SignupForm
import allauth
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserCreationForm(allauth.account.forms.SignupForm):
    first_name = forms.CharField(max_length=20, label='Name', widget=forms.TextInput(attrs={'placeholder':'Name'}))
    def save(self, request):
        user = super(CustomUserCreationForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.save()
        return user

class CustomSocialSignupForm(SignupForm):
    username = forms.CharField(max_length=20, label='Username')
    first_name = forms.CharField(max_length=20, label='Name')
    email = forms.EmailField(widget=forms.HiddenInput())
    def save(self, request):
        user = super(CustomSocialSignupForm, self).save(request)
        user.active_email = True
        user.save()
        return user

class CustomUserChangeForm(forms.Form):
    name = forms.CharField(max_length=25, label="New name")