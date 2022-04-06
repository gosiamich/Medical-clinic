from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


def validate_length(password):
    return len(password) >= 7

def validate_upper(password):
    return any(x for x in password if x.isupper())

def validate_lower(password):
    return any(x for x in password if x.islower())

def validate_special(password):
    special = """!@#$%^&*()_+=-~{}[]:"|;'\<>?,./\|"""
    return any(x for x in password if x in special)

def validate_digit(password):
    return any(x for x in password if x.isdigit())

def validate_password(password):
    validators = [
            validate_digit,
            validate_special,
            validate_lower,
            validate_upper,
            validate_length
        ]
    for validator in validators:
        if not validator(password):
            return False
        return True



class CreateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password':forms.PasswordInput,
            'email': forms.EmailInput,
        }

    def clean_password(self):
        if not validate_password(self.cleaned_data['password']):
            raise ValidationError('Wrong password')
        return self.cleaned_data['password']


