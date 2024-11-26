from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from orders.forms import OrderForm
from orders.models import CITY_CHOICES, VILLAGE_CHOICES
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    if request.method == "POST":
        selected_size = request.POST.get('size')  # Lấy giá trị của kích cỡ đã chọn

        if selected_size:
            # Lấy biến thể kích cỡ phù hợp
            size_variations = Variation.objects.filter(
                product=product,
                variation_value='size',  # Chọn loại biến thể là kích cỡ
                variation_size=selected_size,
            )
            if size_variations.exists():
                product_variation.append(size_variations.first())  # Thêm biến thể kích cỡ vào danh sách

    # Tạo hoặc lấy giỏ hàng theo session
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    if current_user.is_authenticated:
        # Kiểm tra xem CartItem đã tồn tại trong giỏ hàng của người dùng chưa
        cart_items = CartItem.objects.filter(product=product, user=current_user, cart=cart)
    else:
        # Nếu người dùng không đăng nhập, tìm CartItem theo session
        cart_items = CartItem.objects.filter(product=product, cart=cart)

    # Kiểm tra xem sản phẩm có biến thể giống nhau đã có trong giỏ hàng chưa
    existing_cart_item = None
    for item in cart_items:
        # Lấy tất cả các biến thể của CartItem
        item_variations = item.variations.all()
        if selected_size:
            if selected_size == item_variations.filter(variation_value='size').first().variation_size:
                existing_cart_item = item
                break

    if existing_cart_item:
        # Nếu đã có cùng biến thể, kiểm tra tồn kho trước khi tăng số lượng
        variation = Variation.objects.filter(
            product=product,
            variation_size=selected_size
        ).first()

        if variation and existing_cart_item.cart_item_quantity + 1 > variation.stock:
            messages.error(request, "Số lượng vượt quá sản phẩm hiện có.")
        else:
            existing_cart_item.cart_item_quantity += 1
            existing_cart_item.save()
    else:
        # Nếu chưa có, tạo mới CartItem
        cart_item = CartItem.objects.create(
            product=product,
            cart_item_quantity=1,
            user=current_user if current_user.is_authenticated else None,
            cart=cart,  # Gán Cart vào CartItem
        )
        # Lưu các biến thể vào CartItem
        if product_variation:
            cart_item.variations.add(*product_variation)  # Thêm các variations vào CartItem
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
        if cart_item_quantity <= 1: 
           tax = (2 * total) / 100
        else:
           tax = 0
        grand_total = total + tax
        grand_total = round(grand_total)
        tax_display = str(int(tax)) if tax == int(tax) else str(tax)
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'cart_item_quantity': cart_item_quantity,
        'cart_items': cart_items,
        'tax': tax_display if tax > 0 else 'Miễn phí',
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
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'cart_item_quantity': cart_item_quantity,
        'cart_items': cart_items,
        'tax': tax,
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