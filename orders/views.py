import datetime
from django.shortcuts import render, redirect

from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order

def place_order(request, total=0, cart_item_quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.product_price * cart_item.cart_item_quantity)
        cart_item_quantity += cart_item.cart_item_quantity
    if cart_item_quantity > 1:
        tax = 0
    else:
        tax = (2 * total) / 100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.order_first_name = form.cleaned_data['order_first_name']
            data.order_last_name = form.cleaned_data['order_last_name']
            data.order_email = form.cleaned_data['order_email']
            data.order_phone = form.cleaned_data['order_phone']
            data.order_country = form.cleaned_data['order_country']            
            data.order_city = form.cleaned_data['order_city']
            data.order_village = form.cleaned_data['order_village']
            data.order_address = form.cleaned_data['order_address']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.order_tax = tax
            data.order_ip = request.META.get('REMOTE_ADDR')
            data.save()
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('checkout')
        else:
            return redirect('checkout')

    return render(request, 'orders/checkout.html')