from django import forms
from .models import Item, Trip
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import get_user_model

User = get_user_model()

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'is_packed']

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['name', 'destination', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
     