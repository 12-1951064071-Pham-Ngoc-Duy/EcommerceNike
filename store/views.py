from django.http import HttpResponse
from django.shortcuts import render,redirect , get_object_or_404
from django.db.models import Q
from carts.models import CartItem
from orders.models import OrderProduct
from store.forms import ReviewForm
from .models import Product, ProductGallery, ReviewRating
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from django.contrib import messages

def store(request, category_slug_path=None):
    categories = None
    products = None
    if category_slug_path != None:
        categories = get_object_or_404(Category, category_slug=category_slug_path)
        products = Product.objects.filter(category=categories, product_is_availabel=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(product_is_availabel=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    
    context = {
        'products': paged_products,
        'product_count':product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug_path, product_slug_path):
    try:
        single_product = Product.objects.get(category__category_slug = category_slug_path, product_slug=product_slug_path)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
    
    #get the reivew
    reviews = ReviewRating.objects.filter(product_id=single_product.id, review_status=True)

    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct':orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    products = Product.objects.order_by('-product_created_date')
    product_count_result = products.count()

    keyword = request.GET.get('keyword', '')
    if keyword:
        products = products.filter(
            Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword)
        )
        product_count_result = products.count()

    # Thêm phần phân trang
    paginator = Paginator(products, 6)  # 6 sản phẩm mỗi trang
    page = request.GET.get('page', 1)  # Lấy số trang từ request

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)  # Nếu không phải số nguyên, quay về trang 1
    except EmptyPage:
        products = paginator.page(paginator.num_pages)  # Nếu vượt quá số trang, lấy trang cuối

    context = {
        'products': products,
        'product_count_result': product_count_result,
    }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.review_subject = form.cleaned_data['review_subject']
                data.review_rating = form.cleaned_data['review_rating']
                data.review = form.cleaned_data['review']
                data.review_ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)