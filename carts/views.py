from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from orders.forms import OrderForm
from orders.models import CITY_CHOICES, VILLAGE_CHOICES
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import json
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass


        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []
            for item in cart_item:
                exitsting_variation = item.variations.all()
                ex_var_list.append(list(exitsting_variation))
                id.append(item.id)
            
            if product_variation in ex_var_list:
                 index = ex_var_list.index(product_variation)
                 item_id = id[index]
                 item = CartItem.objects.get(product=product, id=item_id)
                 item.cart_item_quantity += 1
                 item.save()
            else:
                item = CartItem.objects.create(product=product, cart_item_quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                cart_item_quantity = 1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    else:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            ex_var_list = []
            id = []
            for item in cart_item:
                exitsting_variation = item.variations.all()
                ex_var_list.append(list(exitsting_variation))
                id.append(item.id)
            print(ex_var_list)
            
            if product_variation in ex_var_list:
                 index = ex_var_list.index(product_variation)
                 item_id = id[index]
                 item = CartItem.objects.get(product=product, id=item_id)
                 item.cart_item_quantity += 1
                 item.save()
            else:
                item = CartItem.objects.create(product=product, cart_item_quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                cart_item_quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart= cart, id=cart_item_id)
        if cart_item.cart_item_quantity > 1:
            cart_item.cart_item_quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, cart_item_quantity=0, cart_items=None, tax=0, grand_total=0):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, cart_item_is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, cart_item_is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.cart_item_quantity)
            cart_item_quantity += cart_item.cart_item_quantity
        if cart_item_quantity > 1:
            tax = 0
        else:
            tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'cart_item_quantity': cart_item_quantity,
        'cart_items': cart_items,
        'tax': tax if tax > 0 else 'Free',
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, cart_item_quantity=0, cart_items=None, tax = 0, grand_total=0):
    form = OrderForm()
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, cart_item_is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, cart_item_is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.cart_item_quantity)
            cart_item_quantity += cart_item.cart_item_quantity
        if cart_item_quantity > 1:
            tax = 0
        else:
            tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'cart_item_quantity': cart_item_quantity,
        'cart_items': cart_items,
        'tax': tax if tax > 0 else 'Free',
        'grand_total': grand_total,
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)

def load_cities_order(request):
    order_country = request.GET.get('order_country')
    cities = CITY_CHOICES.get(order_country, [])
    cities_list = [(order_city[0], order_city[1]) for order_city in cities]
    return JsonResponse({'cities': cities_list})

def load_villages_order(request):
    order_city = request.GET.get('order_city')
    villages = VILLAGE_CHOICES.get(order_city, [])
    villages_list = [(order_village[0], order_village[1]) for order_village in villages]
    return JsonResponse({'villages': villages_list})