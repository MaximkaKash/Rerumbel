from django.contrib.auth.models import User

from django import forms
from django import forms


class RegistrationForm(forms.Form):
    password = forms.CharField(max_length=10)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)


class BasketForm(forms.Form):
    username = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    ch = forms.BooleanField(required=False)
    address = forms.CharField(required=True)
    comment = forms.CharField(required=False)


class LoginForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)


class filter_form(forms.Form):
    category = forms.CharField(max_length=30, required=False)
    way = forms.CharField(max_length=30, required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 101)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
