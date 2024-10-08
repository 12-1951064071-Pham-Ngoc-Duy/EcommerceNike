from django import forms
from .models import Account, UserProfile

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

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

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
