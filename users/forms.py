from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, label="Ism")  # Optional

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu email allaqachon ro'yxatdan o'tgan.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # Set username to email
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    # Override password validation to allow any password
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar mos kelmadi.")
        return password2

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'email']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
