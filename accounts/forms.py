import re
from django import forms
from .models import Account, UserProfile
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Email does not exist.")
        
        return email

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        label="New Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        label="Confirm Password"
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and len(password) < 8:
            self.add_error('password', "Password must be at least 8 characters long.")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data
    
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

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')

        if new_password and len(new_password) < 8:
            self.add_error('new_password', "New password must be at least 8 characters long.")

        if new_password and confirm_new_password and new_password != confirm_new_password:
            self.add_error('confirm_new_password', "Passwords do not match.")

        return cleaned_data

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter confirm password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'date_of_birth', 'country', 'city', 'village','place']
    
    def clean_place(self):
        place = self.cleaned_data.get('place')
        if not place:
            raise forms.ValidationError("This field is required.")
        return place

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            raise forms.ValidationError("This field is required.")
        today = datetime.today().date()
        if date_of_birth > today:
            raise forms.ValidationError("Date of birth cannot be in the future.")
        age_limit = 18
        minimum_age_date = today - timedelta(days=age_limit * 365)
        if date_of_birth > minimum_age_date:
            raise forms.ValidationError(f"You must be at least {age_limit} years old.")
        max_age = 120
        max_age_date = today - timedelta(days=max_age * 365)
        if date_of_birth < max_age_date:
            raise forms.ValidationError(f"Age cannot be more than {max_age} years.")

        return date_of_birth

    def clean_email(self):
        email = self.cleaned_data.get('email')
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        if not re.match(regex, email):
            raise forms.ValidationError("Invalid email format.")
        if ' ' in email:
            raise forms.ValidationError("Email cannot contain spaces.")
        if len(email) > 254:
            raise forms.ValidationError("Email must not exceed 254 characters.")
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        domain = email.split('@')[-1]
        if '.' not in domain:
            raise forms.ValidationError("Invalid domain in email.")
        if domain.endswith('.'):
            raise forms.ValidationError("Email domain cannot end with a dot.")
        username = email.split('@')[0]
        if not re.match(r'^[a-zA-Z0-9_.+-]+$', username):
            raise forms.ValidationError("Invalid characters in email username.")
        disposable_domains = ['mailinator.com', '10minutemail.com', 'tempmail.com']
        if domain in disposable_domains:
            raise forms.ValidationError("Temporary email addresses are not allowed.")

        return email

    def clean_address(self):
        account_address = self.cleaned_data.get('account_address')
        if not account_address:  # Kiểm tra nếu account_address là None hoặc empty
            raise forms.ValidationError("This field is required.")
        return account_address 
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number is None:
           raise forms.ValidationError("This field is required.")

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not phone_number.startswith("+84"):
            raise forms.ValidationError("Phone number must start with '+84' followed by country code.")
    
        regex = r'^\+?\d+$'
        if not re.match(regex, phone_number):
            raise forms.ValidationError("Phone number must only number")
        
        # Kiểm tra chỉ chứa số sau dấu "+"
        if not phone_number[1:].isdigit():
            raise forms.ValidationError("Phone number must contain only digits after the country code.")
        
        # Kiểm tra độ dài hợp lệ (8-15 số)
        if len(phone_number[1:]) < 11:
            raise forms.ValidationError("Phone number must be between 8 and 15 digits after the country code.")
        
        # Kiểm tra tính hợp lệ bằng thư viện phonenumbers
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid phone number for the given country code.")
        except NumberParseException:
            raise forms.ValidationError("Invalid phone number format.")
        
        # Kiểm tra số điện thoại đã tồn tại
        if Account.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists.")

        
        return phone_number

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if not password:
           raise forms.ValidationError("This field is required.")

        if len(password) < 8:
            raise forms.ValidationError("Password must more than 8 digit")

        if confirm_password is None:
           raise forms.ValidationError("This field is required.")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['country'].widget.attrs['placeholder'] = 'Select Country'
        self.fields['city'].widget.attrs['placeholder'] = 'Select City'
        self.fields['village'].widget.attrs['placeholder'] = 'Select Village'
        self.fields['place'].widget.attrs['placeholder'] = 'Enter Place'
        
        # City and Village will be loaded dynamically so no need to set choices in form
        self.fields['city'].widget.attrs['disabled'] = True
        self.fields['village'].widget.attrs['disabled'] = True
    

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number', 'email')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex, email):
            raise forms.ValidationError("Invalid email format.")
        if ' ' in email:
            raise forms.ValidationError("Email cannot contain spaces.")
        if len(email) > 254:
            raise forms.ValidationError("Email must not exceed 254 characters.")
        domain = email.split('@')[-1]
        if '.' not in domain:
            raise forms.ValidationError("Invalid domain in email.")
        if domain.endswith('.'):
            raise forms.ValidationError("Email domain cannot end with a dot.")
        username = email.split('@')[0]
        if not re.match(r'^[a-zA-Z0-9_.+-]+$', username):
            raise forms.ValidationError("Invalid characters in email username.")
        disposable_domains = ['mailinator.com', '10minutemail.com', 'tempmail.com']
        if domain in disposable_domains:
            raise forms.ValidationError("Temporary email addresses are not allowed.")

        return email
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number is None:
           raise forms.ValidationError("This field is required.")

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not phone_number.startswith("+84"):
            raise forms.ValidationError("Phone number must start with '+84' followed by country code.")
    
        regex = r'^\+?\d+$'
        if not re.match(regex, phone_number):
            raise forms.ValidationError("Phone number must only number")
        
        # Kiểm tra chỉ chứa số sau dấu "+"
        if not phone_number[1:].isdigit():
            raise forms.ValidationError("Phone number must contain only digits after the country code.")
        
        # Kiểm tra độ dài hợp lệ (8-15 số)
        if len(phone_number[1:]) < 11:
            raise forms.ValidationError("Phone number must be between 8 and 15 digits after the country code.")
        
        # Kiểm tra tính hợp lệ bằng thư viện phonenumbers
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid phone number for the given country code.")
        except NumberParseException:
            raise forms.ValidationError("Invalid phone number format.")
        return phone_number
    

class UserProfileForm(forms.ModelForm):
    user_profile_picture = forms.ImageField(required=False, error_messages= {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['user_profile_address', 'user_profile_picture', 'user_profile_country', 'user_profile_city', 'user_profile_village', 'user_profile_date_of_birth']
    def clean_user_profile_address(self):
        user_profile_address = self.cleaned_data.get('user_profile_address')
        if not user_profile_address:
            raise forms.ValidationError("This field is required.")
        return user_profile_address

    def clean_user_profile_date_of_birth(self):
        user_profile_date_of_birth = self.cleaned_data.get('user_profile_date_of_birth')
        if not user_profile_date_of_birth:
            raise forms.ValidationError("This field is required.")
        today = datetime.today().date()
        if user_profile_date_of_birth > today:
            raise forms.ValidationError("Date of birth cannot be in the future.")
        age_limit = 18
        minimum_age_date = today - timedelta(days=age_limit * 365)
        if user_profile_date_of_birth > minimum_age_date:
            raise forms.ValidationError(f"You must be at least {age_limit} years old.")
        max_age = 120
        max_age_date = today - timedelta(days=max_age * 365)
        if user_profile_date_of_birth < max_age_date:
            raise forms.ValidationError(f"Age cannot be more than {max_age} years.")

        return user_profile_date_of_birth
    
class AdminAccountsForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'date_of_birth', 'country', 'city', 'village','place']
    
    def clean_place(self):
        place = self.cleaned_data.get('place')
        if not place:
            raise forms.ValidationError("This field is required.")
        return place

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            raise forms.ValidationError("This field is required.")
        today = datetime.today().date()
        if date_of_birth > today:
            raise forms.ValidationError("Date of birth cannot be in the future.")
        age_limit = 18
        minimum_age_date = today - timedelta(days=age_limit * 365)
        if date_of_birth > minimum_age_date:
            raise forms.ValidationError(f"You must be at least {age_limit} years old.")
        max_age = 120
        max_age_date = today - timedelta(days=max_age * 365)
        if date_of_birth < max_age_date:
            raise forms.ValidationError(f"Age cannot be more than {max_age} years.")

        return date_of_birth

    def clean_email(self):
        email = self.cleaned_data.get('email')
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.email == email:
                return email  # Không kiểm tra nếu email không thay đổi
        if not re.match(regex, email):
            raise forms.ValidationError("Invalid email format.")
        if ' ' in email:
            raise forms.ValidationError("Email cannot contain spaces.")
        if len(email) > 254:
            raise forms.ValidationError("Email must not exceed 254 characters.")
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        domain = email.split('@')[-1]
        if '.' not in domain:
            raise forms.ValidationError("Invalid domain in email.")
        if domain.endswith('.'):
            raise forms.ValidationError("Email domain cannot end with a dot.")
        username = email.split('@')[0]
        if not re.match(r'^[a-zA-Z0-9_.+-]+$', username):
            raise forms.ValidationError("Invalid characters in email username.")
        disposable_domains = ['mailinator.com', '10minutemail.com', 'tempmail.com']
        if domain in disposable_domains:
            raise forms.ValidationError("Temporary email addresses are not allowed.")

        return email

    def clean_address(self):
        account_address = self.cleaned_data.get('account_address')
        if not account_address:  # Kiểm tra nếu account_address là None hoặc empty
            raise forms.ValidationError("This field is required.")
        return account_address 
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number is None:
           raise forms.ValidationError("This field is required.")

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not phone_number.startswith("+84"):
            raise forms.ValidationError("Phone number must start with '+84' followed by country code.")
    
        regex = r'^\+?\d+$'
        if not re.match(regex, phone_number):
            raise forms.ValidationError("Phone number must only number")
        
        # Kiểm tra chỉ chứa số sau dấu "+"
        if not phone_number[1:].isdigit():
            raise forms.ValidationError("Phone number must contain only digits after the country code.")
        
        # Kiểm tra độ dài hợp lệ (8-15 số)
        if len(phone_number[1:]) < 11:
            raise forms.ValidationError("Phone number must be between 8 and 15 digits after the country code.")
        
        # Kiểm tra tính hợp lệ bằng thư viện phonenumbers
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid phone number for the given country code.")
        except NumberParseException:
            raise forms.ValidationError("Invalid phone number format.")
        if self.instance.pk:  # Trường hợp cập nhật thông tin
            if self.instance.phone_number == phone_number:
                return phone_number  # Không kiểm tra nếu số điện thoại không thay đổi
        # Kiểm tra số điện thoại đã tồn tại
        if Account.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Phone number already exists.")

        
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
                "At least one of the following fields must be selected: "
                "'is_active', 'is_admin', 'is_staff', or 'is_superadmin'."
            )

        return cleaned_data