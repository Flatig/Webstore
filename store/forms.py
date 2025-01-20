from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for products...',
                'aria-label': 'Search',
            }
        ),
        label='',
    )
