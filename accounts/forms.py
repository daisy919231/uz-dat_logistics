# accounts/forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
from shipper.models import Shipper
from carrier.models import Driver
from django.contrib.auth import authenticate

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    # shared
    phone_number = forms.CharField(max_length=20, required=False)
    full_name=forms.CharField(max_length=100, required=False)

    # shipper only
    company_name = forms.CharField(max_length=255, required=False)

    # driver only
    license_number = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password1', 'password2', 'role', 'phone_number', 'company_name', 'license_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.role = self.cleaned_data['role']

        if commit:
            user.save()
            print(f"Saving user: {user.username}")
            
            # Only create if related model doesn't exist already
            if user.role == 'shipper':
                if not hasattr(user, 'shipper'):
                    phone = self.cleaned_data.get('phone_number')
                    print("Creating shipper with phone:", phone)

                    shipper = Shipper(
                        user=user,
                        phone_number=phone,
                        full_name=self.cleaned_data.get('full_name'),
                        company_name=self.cleaned_data.get('company_name'),
                    )
                    shipper.save()
                else:
                    print("Shipper already exists for user")

            elif user.role == 'driver':
                if not hasattr(user, 'driver'):
                    driver = Driver(
                        user=user,
                        phone_number=self.cleaned_data.get('phone_number'),
                        full_name=self.cleaned_data.get('full_name'),
                        license_number=self.cleaned_data.get('license_number'),
                    )
                    driver.save()
                else:
                    print("Driver already exists for user")

        return user



class LoginForm(forms.Form):
    username = forms.CharField(label="Username")  # generic label
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Accept and remove 'request'
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user = authenticate(
                request=self.request,
                username=username,
                password=password
            )
            if self.user is None:
                raise forms.ValidationError("Invalid username or password")
            elif not self.user.is_active:
                raise forms.ValidationError("This account is inactive")

        return cleaned_data

    def get_user(self):
        return self.user
