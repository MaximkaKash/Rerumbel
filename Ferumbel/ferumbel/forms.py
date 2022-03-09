from ferumbel.models import ORDER_BY_CHOICES, TYPE_CHOICES
from django.contrib.auth.models import User

from django import forms


class RegistrationForm(forms.Form):
    password = forms.CharField(max_length=10)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)


class BasketForm(forms.Form):
    username = forms.CharField()
    phone = forms.CharField()
    # delivery = forms.BooleanField()
    address = forms.CharField()
    comment = forms.CharField()


class LoginForm(forms.Form):
    login = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)


class filter_form(forms.Form):
    category = forms.CharField(max_length=30)
    way = forms.CharField(max_length=30)
    min_price = forms.IntegerField()
    max_price = forms.IntegerField()


class ProductFiltersForm(forms.Form):
    order_by = forms.ChoiceField(
        choices=ORDER_BY_CHOICES,
        required=False,
    )
    price__gt = forms.IntegerField(
        min_value=0,
        label="Price Min",
        required=False,
    )
    price__lt = forms.IntegerField(
        min_value=0,
        label="Price Max",
        required=False,
    )
    section = forms.ChoiceField(
        choices=TYPE_CHOICES,
        required=False,
    )
