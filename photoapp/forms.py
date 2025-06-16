from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from photoapp.models import CustomUser, Photo

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter your email'}),
            'full_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter your full name'}),
            'password1': forms.PasswordInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Confirm your password'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm'}))

    class Meta:
        model = CustomUser
        fields = ['full_name', 'profile_picture', 'bio']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter your full name'}),
            'bio': forms.Textarea(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Tell us about yourself', 'rows': 4}),
        }

class PhotoUploadForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm'}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter tags (comma-separated)'}))

    class Meta:
        model = Photo
        fields = ['title', 'description', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter photo title'}),
            'description': forms.Textarea(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter photo description', 'rows': 4}),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter your old password'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter your new password'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Confirm your new password'}),
        }

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter your email'})
    )

class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = CustomUser
        fields = ['new_password1', 'new_password2']
        widgets = {
            'new_password1': forms.PasswordInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Enter your new password'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500', 'placeholder': 'Confirm your new password'}),
        }