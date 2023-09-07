from django import forms
from .models import Order

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['amount', 'description', 'card_number', 'expiration_date', 'cvv', 'pix_key']