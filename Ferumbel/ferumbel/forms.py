from ferumbel.models import ORDER_BY_CHOICES, TYPE_CHOICES
from django.contrib.auth.models import User

from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField(max_length=20)


class BasketForm(forms.Form):
    username = forms.TextInput()
    phone = forms.CharField()
    delivery = forms.BooleanField()
    address = forms.TextInput()
    comment = forms.TextInput()


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
