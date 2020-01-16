from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from .models import *

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('prod_id',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('full_name', 'gender', 'address', 'bank_card_id', 'phone_number')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('color', 'price', 'availability', 'pr_type', 'size')

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')