from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from carts.views import _cart_id
from orders.models import Order, OrderProduct
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.http import JsonResponse
from .models import CITY_CHOICES, VILLAGE_CHOICES
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
#Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
import requests
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            date_of_birth = form.cleaned_data['date_of_birth']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            village = form.cleaned_data['village']
            address = form.cleaned_data['address']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email,username=username, password=password, date_of_birth= date_of_birth, country=country, city=city, village=village, address=address)
            user.phone_number = phone_number
            user.save()
            UserProfile.objects.create(
                user=user,
                user_profile_country=country,
                user_profile_city=city,
                user_profile_village=village,
                user_profile_address=address
            )
            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #USER ACTIVATION
            # messages.success(request, 'Thank you for registering with us.We have sent you a verification email to your email address [phamngoczuy1@gmail.com]. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm() 
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if user is not None:
                try:
                    # Xử lý giỏ hàng và các logic khác
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        cart_item = CartItem.objects.filter(user=user)
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.cart_item_quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()
                except:
                    pass
                
                auth_login(request, user)
                messages.success(request, 'You are now logged in.')
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:
                    return redirect('dashboard')
            else:
                messages.error(request, 'Wrong password')
                return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Your are logged out.')
    return redirect('login') 

def load_cities(request):
    country = request.GET.get('country')
    cities = CITY_CHOICES.get(country, [])
    cities_list = [(city[0], city[1]) for city in cities]
    return JsonResponse({'cities': cities_list})

def load_villages(request):
    city = request.GET.get('city')
    villages = VILLAGE_CHOICES.get(city, [])
    villages_list = [(village[0], village[1]) for village in villages]
    return JsonResponse({'villages': villages_list})

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activated link')
        return redirect('register')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expried!')
        return redirect('login')
    
@login_required(login_url='login')
def dashboard(request):
    # Lấy tất cả các đơn hàng của người dùng
    orders = Order.objects.order_by('-order_created_at').filter(user_id=request.user.id, order_is_ordered=True)
    orders_count = orders.count()

    # Kiểm tra sự tồn tại của UserProfile, nếu không có sẽ tạo mới
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }

    # Render trang dashboard với context đã bao gồm các đơn hàng và thông tin UserProfile
    return render(request, 'accounts/dashboard.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            #RESET PASSWORD
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
            #USER ACTIVATION
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

@login_required(login_url= 'login')  
def my_orders(request):
    orders = Order.objects.filter(user=request.user, order_is_ordered=True).order_by('-order_created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_order.html', context)

@login_required(login_url= 'login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    current_country = userprofile.user_profile_country
    current_city = userprofile.user_profile_city
    current_village = userprofile.user_profile_village

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'current_country': current_country,
        'current_city': current_city,
        'current_village': current_village,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)



def get_cities(request):
    country = request.GET.get('country')
    cities = CITY_CHOICES.get(country, [])
    cities_list = [(city[0], city[1]) for city in cities]
    return JsonResponse({'cities': cities_list})

def get_villages(request):
    city = request.GET.get('city')
    villages = VILLAGE_CHOICES.get(city, [])
    villages_list = [(village[0], village[1]) for village in villages]
    return JsonResponse({'villages': villages_list})

@login_required(login_url= 'login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_new_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not math!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')

@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.order_product_price * i.order_product_quantity
    context = {
        'order_detail':order_detail,
        'order': order,
        'subtotal':subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)