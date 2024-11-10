import re
from django import forms
from .models import Account, UserProfile
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Nhập thư điện tử'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Nhập mật khẩu'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex, email):
            raise forms.ValidationError("Sai định dạng thư điện tử")
        if not email:
            raise forms.ValidationError("Chưa điền giá trị")
        if not Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Thư điện tử không tồn tại")
        if '@' not in email:
            raise forms.ValidationError("Sai định dạng thư điện tử")

        # Kiểm tra email có chứa nhiều hơn một ký tự `@`
        if email.count('@') > 1:
            raise forms.ValidationError("Sai định dạng thư điện tử")
        
        return email
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Chưa điền giá trị")
        return password
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name in ['email', 'password']:
            self.fields[field_name].required = False

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        label="Confirm Password"
    )
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Chưa điền giá trị")
        return password
    
    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get('confirm_password')
        if not confirm_password:
            raise forms.ValidationError("Chưa điền giá trị")
        return confirm_password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and len(password) < 8:
            self.add_error('password', "Mật khẩu phải dài hơn 8 ký tự")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Mật khẩu không trùng khớp")

        return cleaned_data
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        for field_name in ['password', 'confirm_password']:
            self.fields[field_name].required = False
    
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Current Password'}),
        label="Current Password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        label="New Password"
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}),
        label="Confirm New Password"
    )
    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not current_password:
            raise forms.ValidationError("Chưa điền giá trị")
        return current_password
    
    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if not new_password:
            raise forms.ValidationError("Chưa điền giá trị")
        return new_password
    
    def clean_confirm_new_password(self):
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if not confirm_new_password:
            raise forms.ValidationError("Chưa điền giá trị")
        return confirm_new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and len(new_password) < 8:
            self.add_error('new_password', "Vui lòng nhập lại mật khẩu phải dài ít nhất 8 ký tự")

        if new_password and confirm_new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "Mật khẩu không khớp")

        return cleaned_data
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field_name in ['current_password', 'new_password', 'confirm_new_password']:
            self.fields[field_name].required = False

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter confirm password'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Nhập thư điện tử'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'date_of_birth', 'country', 'city', 'village','place']
            
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("Chưa điền giá trị")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("Chưa điền giá trị")
        return last_name
    
    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise forms.ValidationError("Chưa điền giá trị")
        return country
    
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:
            raise forms.ValidationError("Chưa điền giá trị")
        return city
    
    def clean_village(self):
        village = self.cleaned_data.get('village')
        if not village:
            raise forms.ValidationError("Chưa điền giá trị")
        return village

    
    def clean_place(self):
        place = self.cleaned_data.get('place')
        if not place:
            raise forms.ValidationError("Chưa điền giá trị")
        return place

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            raise forms.ValidationError("Chưa điền giá trị")
        today = datetime.today().date()
        if date_of_birth > today:
            raise forms.ValidationError("Ngày sinh lớn hơn ngày hiện tại")
        age_limit = 18
        minimum_age_date = today - timedelta(days=age_limit * 365)
        if date_of_birth > minimum_age_date:
            raise forms.ValidationError("Tuổi phải trên 18")
        max_age = 120
        max_age_date = today - timedelta(days=max_age * 365)
        if date_of_birth < max_age_date:
            raise forms.ValidationError("Tuổi phải dưới 120")

        return date_of_birth

    def clean_email(self):
        email = self.cleaned_data.get('email')
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if '@' not in email:
            raise forms.ValidationError("Sai định dạng thư điện tử")

        # Kiểm tra email có chứa nhiều hơn một ký tự `@`
        if email.count('@') > 1:
            raise forms.ValidationError("Sai định dạng thư điện tử")
        if not email:
            raise forms.ValidationError("Chưa điền giá trị")

        if not re.match(regex, email):
            raise forms.ValidationError("Sai định dạng thư điện tử")
        if ' ' in email:
            raise forms.ValidationError("Thư điện tử không được chứa khoảng trống")
        if len(email) > 254:
            raise forms.ValidationError("Thư điện tử không vượt quá 254 ký tự")
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Thư điện tử đã được đăng ký")
        domain = email.split('@')[-1]
        if '.' not in domain:
            raise forms.ValidationError("Thư điện tử có tên miền không hợp lệ")
        if domain.endswith('.'):
            raise forms.ValidationError("Thư điện tử có tên miền không được kết thúc bằng dấu chấm")
        username = email.split('@')[0]
        if not re.match(r'^[a-zA-Z0-9_.+-]+$', username):
            raise forms.ValidationError("Ký tự không hợp lệ trong tên người dùng email.")
        disposable_domains = ['mailinator.com', '10minutemail.com', 'tempmail.com']
        if domain in disposable_domains:
            raise forms.ValidationError("Địa chỉ email tạm thời không được phép.")

        return email

    def clean_address(self):
        account_address = self.cleaned_data.get('account_address')
        if not account_address:  # Kiểm tra nếu account_address là None hoặc empty
            raise forms.ValidationError("Chưa điền giá trị")
        return account_address 
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number is None:
           raise forms.ValidationError("Chưa điền giá trị")

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not phone_number.startswith("+"):
            raise forms.ValidationError("Số điện thoại phải bắt đầu bằng dấu (+) trước mã số đất nước của bạn")
    
        regex = r'^\+?\d+$'
        if not re.match(regex, phone_number):
            raise forms.ValidationError("Số điện thoại chỉ có duy nhất là số và không có ký tự đặc biệt ,dấu cách")
        
        # Kiểm tra chỉ chứa số sau dấu "+"
        if not phone_number[1:].isdigit():
            raise forms.ValidationError("Số điện thoại chỉ được chứa các chữ số sau mã số đất nước.")
        
        # Kiểm tra tính hợp lệ bằng thư viện phonenumbers
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Số điện thoại không hợp lệ cho mã số đất nước đã cho.")
        except NumberParseException:
            raise forms.ValidationError("Định dạng số điện thoại không hợp lệ.")
        
        # Kiểm tra số điện thoại đã tồn tại
        if Account.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Số điện thoại đã đăng ký")

        
        return phone_number

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if not password:
            self.add_error('password', "Chưa điền giá trị")
        elif len(password) < 8:
            self.add_error('password', "Mật khẩu lớn hơn 8 ký tự")

        if confirm_password is None:
           raise forms.ValidationError("Chưa điền giá trị")
        elif password != confirm_password:
            self.add_error('password', "Mật khẩu chưa khớp")
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nhập tên đầu'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Nhập tên cuối'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Nhập số điện thoại'
        self.fields['email'].widget.attrs['placeholder'] = 'Nhập thư điện tử'
        self.fields['password'].widget.attrs['placeholder'] = 'Nhập mật khẩu'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Nhập lại mật khẩu'
        self.fields['country'].widget.attrs['placeholder'] = 'Chọn đất nước'
        self.fields['city'].widget.attrs['placeholder'] = 'Chọn thành phố'
        self.fields['village'].widget.attrs['placeholder'] = 'Chọn huyện'
        self.fields['place'].widget.attrs['placeholder'] = 'Chọn địa chỉ'
        
        # City and Village will be loaded dynamically so no need to set choices in form
        self.fields['city'].widget.attrs['disabled'] = True
        self.fields['village'].widget.attrs['disabled'] = True
        for field_name in ['first_name', 'last_name', 'country', 'email', 'password', 'confirm_password']:
            self.fields[field_name].required = False
    

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number', 'email')
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
           raise forms.ValidationError("Chưa điền giá trị")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
           raise forms.ValidationError("Chưa điền giá trị")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not email:
           raise forms.ValidationError("Chưa điền giá trị")
        if not re.match(regex, email):
            raise forms.ValidationError("Định dạng thư điện tử không hợp lệ.")
        if ' ' in email:
            raise forms.ValidationError("Thư điện tử không được chứa dấu cách.")
        if len(email) > 254:
            raise forms.ValidationError("Thư điện tử không được vượt quá 254 ký tự.")
        domain = email.split('@')[-1]
        if '.' not in domain:
            raise forms.ValidationError("Tên miền không hợp lệ trong email.")
        if domain.endswith('.'):
            raise forms.ValidationError("Tên miền thư điện tử không thể kết thúc bằng dấu chấm.")
        username = email.split('@')[0]
        if not re.match(r'^[a-zA-Z0-9_.+-]+$', username):
            raise forms.ValidationError("Ký tự không hợp lệ trong tên người dùng thư điện tử.")
        disposable_domains = ['mailinator.com', '10minutemail.com', 'tempmail.com']
        if domain in disposable_domains:
            raise forms.ValidationError("Địa chỉ email tạm thời không được phép.")
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.email == email:
                return email  # Không kiểm tra nếu email không thay đổi
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Thư điện tử này đã tồn tại.")

        return email
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number:
           raise forms.ValidationError("Chưa điền giá trị")

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not phone_number.startswith("+"):
            raise forms.ValidationError("Số điện thoại phải bắt đầu bằng '+', sau đó là mã đất nước.")
    
        regex = r'^\+?\d+$'
        if not re.match(regex, phone_number):
            raise forms.ValidationError("Số điện thoại chỉ được có số")
        
        # Kiểm tra chỉ chứa số sau dấu "+"
        if not phone_number[1:].isdigit():
            raise forms.ValidationError("Số điện thoại chỉ được chứa các chữ số sau mã đất nước.")
        
        # Kiểm tra tính hợp lệ bằng thư viện phonenumbers
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Số điện thoại không hợp lệ cho mã đất nước đã cho.")
        except NumberParseException:
            raise forms.ValidationError("Định dạng số điện thoại không hợp lệ.")

        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.phone_number == phone_number:
                return phone_number  # Không kiểm tra nếu số điện thoại không thay đổi
        # Kiểm tra số điện thoại đã tồn tại
        if Account.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Số điện thoại đã tồn tại.")
        return phone_number
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field_name in ['first_name', 'last_name','email', 'phone_number']:
            self.fields[field_name].required = False
    

class UserProfileForm(forms.ModelForm):
    user_profile_picture = forms.ImageField(required=False, error_messages= {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['user_profile_address', 'user_profile_picture', 'user_profile_country', 'user_profile_city', 'user_profile_village', 'user_profile_date_of_birth']
    def clean_user_profile_address(self):
        user_profile_address = self.cleaned_data.get('user_profile_address')
        if not user_profile_address:
            raise forms.ValidationError("Chưa điền giá trị")
        return user_profile_address
    
    def clean_user_profile_country(self):
        user_profile_country = self.cleaned_data.get('user_profile_country')
        if not user_profile_country:
            raise forms.ValidationError("Chưa điền giá trị")
        return user_profile_country
    
    def clean_user_profile_city(self):
        user_profile_city = self.cleaned_data.get('user_profile_city')
        if not user_profile_city:
            raise forms.ValidationError("Chưa điền giá trị")
        return user_profile_city
    
    def clean_user_profile_village(self):
        user_profile_village = self.cleaned_data.get('user_profile_village')
        if not user_profile_village:
            raise forms.ValidationError("Chưa điền giá trị")
        return user_profile_village
    
    def clean_user_profile_picture(self):
        user_profile_picture = self.cleaned_data.get('user_profile_picture')
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.user_profile_picture == user_profile_picture:
                return user_profile_picture  # Không kiểm tra nếu số điện thoại không thay đổi
        if not user_profile_picture:
            raise forms.ValidationError("Chưa điền giá trị")
        return user_profile_picture

    def clean_user_profile_date_of_birth(self):
        user_profile_date_of_birth = self.cleaned_data.get('user_profile_date_of_birth')
        if not user_profile_date_of_birth:
            raise forms.ValidationError("Chưa điền giá trị")
        today = datetime.today().date()
        if user_profile_date_of_birth > today:
            raise forms.ValidationError("Ngày sinh không thể ở trong tương lai.")
        age_limit = 18
        minimum_age_date = today - timedelta(days=age_limit * 365)
        if user_profile_date_of_birth > minimum_age_date:
            raise forms.ValidationError("Tuổi lớn hơn 18")
        max_age = 120
        max_age_date = today - timedelta(days=max_age * 365)
        if user_profile_date_of_birth < max_age_date:
            raise forms.ValidationError("Tuổi nhỏ hơn 120")
        return user_profile_date_of_birth
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name in ['user_profile_date_of_birth', 'user_profile_picture','user_profile_country', 'user_profile_city', 'user_profile_village', 'user_profile_address']:
            self.fields[field_name].required = False
    
class AdminAccountsForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'date_of_birth', 'country', 'city', 'village','place']
    
    def clean_place(self):
        place = self.cleaned_data.get('place')
        if not place:
            raise forms.ValidationError("Trường này là bắt buộc")
        return place

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            raise forms.ValidationError("Trường này là bắt buộc")
        today = datetime.today().date()
        if date_of_birth > today:
            raise forms.ValidationError("Ngày sinh lớn hơn ngày hiện tại")
        age_limit = 18
        minimum_age_date = today - timedelta(days=age_limit * 365)
        if date_of_birth > minimum_age_date:
            raise forms.ValidationError("Ngày sinh phải lớn hơn 18")
        max_age = 120
        max_age_date = today - timedelta(days=max_age * 365)
        if date_of_birth < max_age_date:
            raise forms.ValidationError("Ngày sinh phải nhỏ hơn 120")

        return date_of_birth

    def clean_email(self):
        email = self.cleaned_data.get('email')
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if not re.match(regex, email):
            raise forms.ValidationError("Cấu trúc thư điện tử không đúng")
        if ' ' in email:
            raise forms.ValidationError("Thư điện tử không chứa dấu cách")
        if len(email) > 254:
            raise forms.ValidationError("Thư điện tử không quá 254 ký tự")
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.email == email:
                return email  # Không kiểm tra nếu email không thay đổi
        elif Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Thư điện tử đã đăng ký")
        domain = email.split('@')[-1]
        if '.' not in domain:
            raise forms.ValidationError("Tên miền thư điện tử không hợp lệ")
        if domain.endswith('.'):
            raise forms.ValidationError("Tên miền thư điện tử không kết thúc bằng dấu chấm")
        username = email.split('@')[0]
        if not re.match(r'^[a-zA-Z0-9_.+-]+$', username):
            raise forms.ValidationError("Ký tự không hợp lệ trong thư điện tử người dùng")
        disposable_domains = ['mailinator.com', '10minutemail.com', 'tempmail.com']
        if domain in disposable_domains:
            raise forms.ValidationError("Địa chỉ email tạm thời không được phép.")

        return email

    def clean_address(self):
        account_address = self.cleaned_data.get('account_address')
        if not account_address:  # Kiểm tra nếu account_address là None hoặc empty
            raise forms.ValidationError("Trường này là bắt buộc")
        return account_address 
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number is None:
           raise forms.ValidationError("Trường này là bắt buộc")

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not phone_number.startswith("+"):
            raise forms.ValidationError("Số điện thoại phải bắt đầu bằng '+', sau đó là mã quốc gia.")
    
        regex = r'^\+?\d+$'
        if not re.match(regex, phone_number):
            raise forms.ValidationError("Số điện thoại chỉ được có số")
        
        # Kiểm tra chỉ chứa số sau dấu "+"
        if not phone_number[1:].isdigit():
            raise forms.ValidationError("Số điện thoại chỉ được chứa các chữ số sau mã quốc gia.")
        
        # # Kiểm tra độ dài hợp lệ (8-15 số)
        # if len(phone_number[1:]) < 11:
        #     raise forms.ValidationError("Phone number must be between 8 and 15 digits after the country code.")
        
        # Kiểm tra tính hợp lệ bằng thư viện phonenumbers
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Số điện thoại không hợp lệ cho mã quốc gia đã cho.")
        except NumberParseException:
            raise forms.ValidationError("Định dạng số điện thoại không hợp lệ.")
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.phone_number == phone_number:
                return phone_number  # Không kiểm tra nếu số điện thoại không thay đổi
        # Kiểm tra số điện thoại đã tồn tại
        if Account.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Số điện thoại đã đăng ký.")

        
        return phone_number
    def clean(self):
        cleaned_data = super().clean()
        is_active = cleaned_data.get('is_active')
        is_admin = cleaned_data.get('is_admin')
        is_staff = cleaned_data.get('is_staff')
        is_superadmin = cleaned_data.get('is_superadmin')

        # Kiểm tra nếu tất cả các trường này đều không được chọn
        if not any([is_active, is_admin, is_staff, is_superadmin]):
            raise forms.ValidationError(
                "Ít nhất một trong các trường sau phải được chọn:"
                "'Quyền hoạt động', 'Quyền quản trị viên', 'Quyền nhân viên' hoặc 'Quyền siêu quản trị viên'."
            )

        return cleaned_data

class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_profile_address', 'user_profile_picture', 'user_profile_country', 'user_profile_city', 'user_profile_village', 'user_profile_date_of_birth']
    def clean_user_profile_address(self):
        user_profile_address = self.cleaned_data.get('user_profile_address')
        if not user_profile_address:
            raise forms.ValidationError("Trường này là bắt buộc")
        return user_profile_address
    
    def clean_user_profile_country(self):
        user_profile_country = self.cleaned_data.get('user_profile_country')
        if not user_profile_country:
            raise forms.ValidationError("Trường này là bắt buộc")
        return user_profile_country
    
    def clean_user_profile_city(self):
        user_profile_city = self.cleaned_data.get('user_profile_city')
        if not user_profile_city:
            raise forms.ValidationError("Trường này là bắt buộc")
        return user_profile_city
    
    def clean_user_profile_village(self):
        user_profile_village = self.cleaned_data.get('user_profile_village')
        if not user_profile_village:
            raise forms.ValidationError("Trường này là bắt buộc")
        return user_profile_village

    def clean_user_profile_picture(self):
        user_profile_picture = self.cleaned_data.get('user_profile_picture')
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.user_profile_picture == user_profile_picture:
                return user_profile_picture  # Không kiểm tra nếu số điện thoại không thay đổi
        if not user_profile_picture:
            raise forms.ValidationError("Trường này là bắt buộc")
        return user_profile_picture

    def clean_user_profile_date_of_birth(self):
        user_profile_date_of_birth = self.cleaned_data.get('user_profile_date_of_birth')
        if not user_profile_date_of_birth:
            raise forms.ValidationError("Trường này là bắt buộc")
        today = datetime.today().date()
        if user_profile_date_of_birth > today:
            raise forms.ValidationError("Ngày sinh không thể ở trong tương lai.")
        age_limit = 18
        minimum_age_date = today - timedelta(days=age_limit * 365)
        if user_profile_date_of_birth > minimum_age_date:
            raise forms.ValidationError("Tuổi phải lớn hơn 18")
        max_age = 120
        max_age_date = today - timedelta(days=max_age * 365)
        if user_profile_date_of_birth < max_age_date:
            raise forms.ValidationError("Tuổi phải nhỏ hơn 120")

        return user_profile_date_of_birth