from django import forms
from django.forms import widgets

class SignupForm(forms.Form):
    dob=forms.DateField(label='Date of Birth: ',widget=widgets.DateInput(attrs={'type':'date'}))
    company=forms.CharField(label='Company: ', max_length=50)
    profile_img=forms.ImageField(label='')
    phone=forms.CharField(max_length=13)
    location=forms.CharField(max_length=25)
