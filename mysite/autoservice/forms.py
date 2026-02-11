from .models import OrderReview, CustomUser, Order, OrderLine
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

class OrderCreateUpdateForm(forms.ModelForm):
    """Forma užsakymo kūrimui ir redagavimui"""
    class Meta:
        model = Order
        fields = ['car', 'due_back', 'status']
        widgets = {
            'due_back': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class OrderLineForm(forms.ModelForm):
    """Forma užsakymo eilutei"""
    class Meta:
        model = OrderLine
        fields = ['service', 'quantity']
