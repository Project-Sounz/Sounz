from django import forms
from .models import profiledatadb

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = profiledatadb
        fields = [ 'profile_picture']
        exclude=['username', 'password', 'email', 'firstname', 'lastname','user_bio', 'phone']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = profiledatadb
        fields = ['username', 'firstname', 'lastname','email','profile_picture', 'user_bio']
        exclude=['password','phone']