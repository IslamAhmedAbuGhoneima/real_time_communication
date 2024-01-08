from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from account.models import User


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-4 px-2 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500'
            }),
        }


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role']
        widgets = {
            'email': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full py-4 px-6 rounded-xl border'
            })
        }
