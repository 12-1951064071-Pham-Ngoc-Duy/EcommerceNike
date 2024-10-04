from django.shortcuts import render, redirect

from orders.forms import OrderForm

def place_order(request):
    
    return render(request, 'orders/checkout.html')