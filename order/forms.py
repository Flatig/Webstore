from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'address', 'city']

        labels = {
            'name': 'Name',
            'email': 'Email',
            'address': 'Address',
            'city': 'City',
        }
        help_texts = {
            'name': 'Please enter your full name.',
            'email': 'We will send the confirmation to this email.',
            'address': 'Enter the delivery address.',
            'city': 'Specify the city of delivery.',
        }
        widgets = {
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'address': forms.TextInput(),
            'city': forms.TextInput(),
        }