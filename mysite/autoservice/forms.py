from .models import OrderReview, CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ['content']

class CustomUserChangeForm(forms.ModelForm):
    """Forma profilio redagavimui"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo']

class CustomUserCreationForm(UserCreationForm):
    """Forma registracijai su CustomUser"""
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
