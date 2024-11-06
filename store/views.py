from django.http import HttpResponse
from django.shortcuts import render,redirect , get_object_or_404
from django.db.models import Q
from carts.models import CartItem
from orders.models import OrderProduct
from store.forms import ReviewForm
from .models import GENDER_CHOICES, Product, ProductGallery, ReviewRating
from category.models import Category
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger,Paginator
from django.contrib import messages

def store_by_gender(request, gender):
    products = Product.objects.filter(product_is_availabel=True, product_gender=gender)

    # Phân trang
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    # Tạo context
    context = {
        'products': paged_products,
        'product_count': product_count,
        'links': Category.objects.all(),  # Để hiển thị danh sách categories
        'selected_genders': [gender],  # Để đánh dấu giới tính đang chọn
    }

    return render(request, 'store/store.html', context)

def store(request, category_slug_path=None):
    categories = None
    products = Product.objects.filter(product_is_availabel=True)

    # Lấy danh sách các checkbox được chọn từ request
    selected_categories = request.GET.getlist('category')  # Lấy category từ request
    selected_genders = request.GET.getlist('gender')      # Lấy gender từ request

    # Kiểm tra nếu 'all' được chọn
    if 'all' in selected_categories:
        selected_categories = []  # Đặt selected_categories thành rỗng để không lọc theo category

    # Lọc theo các checkbox đã chọn trong Categories
    if selected_categories:
        products = products.filter(category__category_slug__in=selected_categories)
    elif category_slug_path:  # Kiểm tra category_slug_path
        products = products.filter(category__category_slug=category_slug_path)  # Lọc theo category_slug_path

    # Lọc theo các checkbox đã chọn trong Gender
    if selected_genders:
        products = products.filter(product_gender__in=selected_genders)

    # Phân trang
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()

    # Tạo context
    context = {
        'products': paged_products,
        'product_count': product_count,
        'links': Category.objects.all(),  # Để hiển thị danh sách categories
        'GENDER_CHOICES': GENDER_CHOICES,  # Truyền GENDER_CHOICES vào context
        'selected_categories': selected_categories,  # Truyền danh sách category đã chọn vào context
        'selected_genders': selected_genders,  # Truyền danh sách gender đã chọn vào context
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
    product_count = products.count()

    keyword = request.GET.get('keyword', '')
    if keyword:
        products = products.filter(
            Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword)
        )
        product_count = products.count()

    paginator = Paginator(products, 6)
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,  # Thêm keyword vào context
    }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id = request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Cảm ơn! Đánh giá của bạn đã được cập nhật.')
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
                messages.success(request, 'Cảm ơn! Đánh giá của bạn đã được gửi.')
                return redirect(url)