from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text='Required: Your password must be at least 8 characters long.'
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput,
        help_text='Required: Enter the same password as before, for verification.'
    )
    image = forms.ImageField(
        label='Profile Image',
        required=False,
        help_text='Optional: Upload a profile image (JPEG, PNG format).'
    )
    date_of_birth = forms.DateField(
        label='Date of Birth',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Optional: Please enter your date of birth in YYYY-MM-DD format.'
    )

    class Meta:
        model = User  # The form is associated with the User model
        fields = ['username', 'email', 'password', 'password2', 'image', 'date_of_birth']
        help_texts = {
            'username': 'Required: Choose a unique username for your account.',
            'email': 'Required: Enter a valid email address. This will be used for account recovery.',
        }

    # Length check.
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')
        return password

    # Match check.
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    # Email uniqueness check.
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data


# The classes UserEditForm and ProfileEditForm are designed to separate the logic for editing user data and the user’s profile.
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    # Email uniqueness check.
    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id) \
            .filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'image']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }