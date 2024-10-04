from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_first_name', 'order_last_name', 'order_phone','order_email','order_address','order_country','order_city','order_village','order_note']