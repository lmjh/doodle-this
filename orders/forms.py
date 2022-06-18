from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    A form to collect the user's personal details during checkout
    """
    class Meta:
        model = Order
        fields = (
            'first_name',
            'last_name',
            'address_1',
            'address_2',
            'town',
            'county',
            'postcode',
            'country',
            'email_address',
            'phone_number',
        )
