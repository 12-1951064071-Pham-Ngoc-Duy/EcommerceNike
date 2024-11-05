from django import forms
from .models import Order
from .models import Account
import re
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['order_first_name', 'order_last_name', 'order_phone','order_email','order_address','order_country','order_city','order_village','order_note']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['order_first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['order_last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['order_phone'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['order_email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['order_address'].widget.attrs['placeholder'] = 'Enter Address'
        self.fields['order_country'].widget.attrs['placeholder'] = 'Select Country'
        self.fields['order_city'].widget.attrs['placeholder'] = 'Select City'
        self.fields['order_village'].widget.attrs['placeholder'] = 'Select Village'
        
        # City and Village will be loaded dynamically so no need to set choices in form
        self.fields['order_city'].widget.attrs['disabled'] = True
        self.fields['order_village'].widget.attrs['disabled'] = True

    def clean_order_first_name(self):
        first_name = self.cleaned_data.get('order_first_name')
        if not first_name:
            raise forms.ValidationError("This field is required.")
        if not re.match("^[A-Za-z]+$", first_name):
            raise forms.ValidationError("First name should only contain letters.")
        return first_name

    def clean_order_last_name(self):
        last_name = self.cleaned_data.get('order_last_name')
        if not last_name:
            raise forms.ValidationError("This field is required.")
        if not re.match("^[A-Za-z]+$", last_name):
            raise forms.ValidationError("Last name should only contain letters.")
        return last_name

    def clean_order_phone(self):
        phone = self.cleaned_data.get('order_phone')
        if phone is None:
           raise forms.ValidationError("This field is required.")
        else:
           # Loại bỏ dấu cách và các ký tự không mong muốn
           phone = re.sub(r'[^\d+]', '', phone)

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not phone.startswith("+"):
            raise forms.ValidationError("Phone number must start with '+' followed by country code.")
        
        # Kiểm tra chỉ chứa số sau dấu "+"
        if not phone[1:].isdigit():
            raise forms.ValidationError("Phone number must contain only digits after the country code.")
        
        # Kiểm tra độ dài hợp lệ (8-15 số)
        if len(phone[1:]) < 11:
            raise forms.ValidationError("Phone number must be between 8 and 15 digits after the country code.")
        
        # Kiểm tra tính hợp lệ bằng thư viện phonenumbers
        try:
            parsed_number = phonenumbers.parse(phone, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid phone number for the given country code.")
        except NumberParseException:
            raise forms.ValidationError("Invalid phone number format.")
        return phone

    def clean_order_email(self):
        email = self.cleaned_data.get('order_email')
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

    def clean_order_address(self):
        address = self.cleaned_data.get('order_address')
        if not address:
            raise forms.ValidationError("This field is required.")
        return address

    def clean_order_country(self):
        country = self.cleaned_data.get('order_country')
        if not country:
            raise forms.ValidationError("This field is required.")
        return country

    def clean_order_city(self):
        order_city = self.cleaned_data.get('order_city')
        if not order_city:
            raise forms.ValidationError("This field is required.")
        return order_city
    
    def clean_order_village(self):
        order_village = self.cleaned_data.get('order_village')
        if not order_village:
            raise forms.ValidationError("This field is required.")
        return order_village

    def clean_order_note(self):
        note = self.cleaned_data.get('order_note')
        if not note:
            raise forms.ValidationError("This field is required.")
        return note

class OrderFormAdmin(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'  # Hoặc bạn có thể chỉ định các trường cụ thể

    def clean(self):
        cleaned_data = super().clean()
        order_status = cleaned_data.get("order_status")
        order_is_ordered = cleaned_data.get("order_is_ordered")

        if order_status == "Delivery Failed" and order_is_ordered:
            raise forms.ValidationError("order_is_ordered is not allowed to be charged when the status is 'Delivery Failed'.")

        if order_status != "Delivery Failed" and not order_is_ordered:
            raise forms.ValidationError("order_is_ordered must be accumulated if the state is not 'Delivery Failed'.")

        return cleaned_data