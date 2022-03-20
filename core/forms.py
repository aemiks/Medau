from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from core.models import Account, PrivateChatRoom
from friends.models import FriendList

class AccountForm(forms.Form):
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'First name'
    }))
    last_name = forms.CharField(max_length=50, required=True,widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Last name'
    }))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Enter your email address'
    }))
    nationality = CountryField(blank_label='( select or update nationality )').formfield(
        required=True,
        widget=CountrySelectWidget(attrs={
            'class' : 'form-control'
        }))

class AccountImageUpdateForm(forms.Form):
    account_image = forms.ImageField(label='Upload avatar', widget=forms.FileInput(attrs={
        'class': 'btn button',}))



