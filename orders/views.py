from django.shortcuts import render, redirect

def place_order(request):
    
    return render(request, 'orders/checkout.html')