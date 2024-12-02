import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order, OrderProduct, Payment
import json
from store.models import Product
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages

from suppliers.models import StockEntry

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, order_is_ordered=False, order_number=body['orderID'])
    
    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid=order.order_total,
        status="Đã thanh toán",
    )
    payment.save()
    order.payment = payment
    order.order_is_ordered = True
    order.save()

    # Chuyển các item trong giỏ hàng sang bảng OrderProduct
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderproduct = OrderProduct() 
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.order_product_quantity = item.cart_item_quantity
        orderproduct.order_product_price = item.product.product_price
        orderproduct.order_product_ordered = True
        orderproduct.save()

        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()

        # Giảm số lượng của từng variation theo FIFO
        for variation in product_variation:
            total_to_deduct = item.cart_item_quantity  # Tổng số lượng cần giảm

    # Lấy tất cả các lô hàng liên quan đến sản phẩm theo FIFO (cũ trước)
            stock_entries = StockEntry.objects.filter(
                product=item.product,
                stock_color=variation.variation_color,
                stock_size=variation.variation_size,
                remaining_quantity__gt=0  # Chỉ lấy các lô còn hàng
            ).order_by('entry_date')  # Sắp xếp theo ngày nhập

    # Giảm tồn kho từ các lô hàng theo thứ tự FIFO
            for stock_entry in stock_entries:
                if total_to_deduct <= 0:
                    break  # Đã giảm hết số lượng cần thiết

        # Xác định số lượng có thể giảm trong lô này
                quantity_to_reduce = min(stock_entry.remaining_quantity, total_to_deduct)
                stock_entry.remaining_quantity -= quantity_to_reduce
                stock_entry.save()

        # Cập nhật số lượng còn cần giảm
                total_to_deduct -= quantity_to_reduce
            variation.stock -= item.cart_item_quantity
            variation.save()

    # Xóa tất cả các CartItem trong giỏ hàng
    CartItem.objects.filter(user=request.user).delete()

    # Gửi email xác nhận
    mail_subject = 'Cảm ơn bạn đã đặt hàng!'
    message = render_to_string('orders/order_recieved_email.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # Gửi lại order_number và transID cho phương thức sendData
    data = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
    }
    return JsonResponse(data)



def place_order(request, total=0, cart_item_quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        product_price = cart_item.product.discounted_price  # Lấy giá giảm hoặc giá gốc
        if product_price is not None:
                total += (product_price * cart_item.cart_item_quantity)
                cart_item_quantity += cart_item.cart_item_quantity
    if cart_item_quantity <= 1: 
           tax = (2 * total) / 100
    else:
           tax = 0
    grand_total = total + tax
    grand_total = round(grand_total)
    tax_display = str(int(tax)) if tax == int(tax) else str(tax)
    
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
            order = Order.objects.get(user=current_user, order_is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax_display if tax > 0 else 0,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
        else:
            context = {
                'form': form,
                'cart_items': cart_items,
                'total': total,
                'tax': tax_display if tax > 0 else 0,
                'grand_total': grand_total,
            }
            return render(request, 'orders/checkout.html', context )
    else:
        form = OrderForm()
    context = {
        'form': form,
    }
    return render(request, 'orders/checkout.html', context)

def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    try:
        order = Order.objects.get(order_number=order_number, order_is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        
        subtotal = 0  # Khởi tạo subtotal

        # Tính toán giá trị sản phẩm sau giảm giá
        for item in ordered_products:
            product = item.product  # Lấy sản phẩm từ đơn hàng
            discount_code = product.discount_code  # Giả sử đây là phần trăm giảm giá, ví dụ: 10%

            # Tính giá sau giảm giá
            if discount_code > 0:
                discount_amount = item.order_product_price * (discount_code / 100)
                discounted_price = item.order_product_price - discount_amount
            else:
                discounted_price = item.order_product_price  # Không có giảm giá

            item.order_product_price = discounted_price * item.order_product_quantity # Cập nhật giá mới cho sản phẩm
            subtotal += item.order_product_price  # Cập nhật subtotal

        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'subtotal': round(subtotal),  # Làm tròn subtotal và gửi tới template
        }
        return render(request, 'orders/order_complete.html', context)
    
    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')

