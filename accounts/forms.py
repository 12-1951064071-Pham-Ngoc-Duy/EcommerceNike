import re
from django import forms
from .models import Account, UserProfile
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter confirm password'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', 'date_of_birth', 'country', 'city', 'village', 'address']

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if address is None:
           raise forms.ValidationError("This field is required.")
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number is None:
           raise forms.ValidationError("This field is required.")
        else:
           # Loại bỏ dấu cách và các ký tự không mong muốn
           phone_number = re.sub(r'[^\d+]', '', phone_number)

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not phone_number.startswith("+"):
            raise forms.ValidationError("Phone number must start with '+' followed by country code.")
        
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
        self.fields['address'].widget.attrs['placeholder'] = 'Enter Address'
        
        # City and Village will be loaded dynamically so no need to set choices in form
        self.fields['city'].widget.attrs['disabled'] = True
        self.fields['village'].widget.attrs['disabled'] = True
    

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number', 'email')

class UserProfileForm(forms.ModelForm):
    user_profile_picture = forms.ImageField(required=False, error_messages= {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['user_profile_address', 'user_profile_picture', 'user_profile_country', 'user_profile_city', 'user_profile_village']
