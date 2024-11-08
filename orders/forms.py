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
        self.fields['order_first_name'].widget.attrs['placeholder'] = 'Nhập tên đầu'
        self.fields['order_last_name'].widget.attrs['placeholder'] = 'Nhập tên cuối'
        self.fields['order_phone'].widget.attrs['placeholder'] = 'Nhập số điện thoại'
        self.fields['order_email'].widget.attrs['placeholder'] = 'Nhập thư điện tử'
        self.fields['order_address'].widget.attrs['placeholder'] = 'Nhập địa chỉ'
        self.fields['order_country'].widget.attrs['placeholder'] = 'Chọn đất nước'
        self.fields['order_city'].widget.attrs['placeholder'] = 'Chọn thành phố'
        self.fields['order_village'].widget.attrs['placeholder'] = 'Chọn huyện'
        
        # City and Village will be loaded dynamically so no need to set choices in form
        self.fields['order_city'].widget.attrs['disabled'] = True
        self.fields['order_village'].widget.attrs['disabled'] = True
        for field_name in ['order_first_name', 'order_last_name', 'order_email', 'order_phone', 'order_country', 'order_address', 'order_note']:
            self.fields[field_name].required = False

    def clean_order_first_name(self):
        first_name = self.cleaned_data.get('order_first_name')
        if not first_name:
            raise forms.ValidationError("Chưa điền giá trị")
        if not re.match("^[A-Za-z]+$", first_name):
            raise forms.ValidationError("Tên chỉ nên chứa các chữ cái.")
        return first_name

    def clean_order_last_name(self):
        last_name = self.cleaned_data.get('order_last_name')
        if not last_name:
            raise forms.ValidationError("Chưa điền giá trị")
        if not re.match("^[A-Za-z]+$", last_name):
            raise forms.ValidationError("Tên chỉ nên chứa các chữ cái.")
        return last_name

    def clean_order_phone(self):
        phone_number = self.cleaned_data.get('order_phone')

        if not phone_number:
           raise forms.ValidationError("Chưa điền giá trị")

        # Kiểm tra số điện thoại bắt đầu bằng "+"
        if not phone_number.startswith("+"):
            raise forms.ValidationError("Số điện thoại phải bắt đầu bằng '+', sau đó là mã đất nước.")

        regex = r'^\+?\d+$'
        if not re.match(regex, phone_number):
            raise forms.ValidationError("Số điện thoại chỉ có duy nhất là số và không có ký tự đặc biệt ,dấu cách")
        
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
        return phone_number

    def clean_order_email(self):
        email = self.cleaned_data.get('order_email')
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
            raise forms.ValidationError("Tên miền không hợp lệ trong thư điện tử.")
        if domain.endswith('.'):
            raise forms.ValidationError("Tên miền thư điện tử không thể kết thúc bằng dấu chấm.")
        username = email.split('@')[0]
        if not re.match(r'^[a-zA-Z0-9_.+-]+$', username):
            raise forms.ValidationError("Ký tự không hợp lệ trong tên người dùng thư điện tử.")
        disposable_domains = ['mailinator.com', '10minutemail.com', 'tempmail.com']
        if domain in disposable_domains:
            raise forms.ValidationError("Địa chỉ email tạm thời không được phép.")
        return email

    def clean_order_address(self):
        address = self.cleaned_data.get('order_address')
        if not address:
            raise forms.ValidationError("Chưa điền giá trị")
        return address

    def clean_order_country(self):
        country = self.cleaned_data.get('order_country')
        if not country:
            raise forms.ValidationError("Chưa điền giá trị")
        return country

    def clean_order_city(self):
        order_city = self.cleaned_data.get('order_city')
        if not order_city:
            raise forms.ValidationError("Chưa điền giá trị")
        return order_city
    
    def clean_order_village(self):
        order_village = self.cleaned_data.get('order_village')
        if not order_village:
            raise forms.ValidationError("Chưa điền giá trị")
        return order_village

    def clean_order_note(self):
        note = self.cleaned_data.get('order_note')
        if not note:
            raise forms.ValidationError("Chưa điền giá trị")
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