from .models import OrderReview
from django import forms
from django.contrib.auth.models import User

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ['content']

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']