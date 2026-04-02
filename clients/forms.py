from django import forms
from django.core.exceptions import ValidationError
from .models import Client
from contacts.models import Contact


class ClientForm(forms.ModelForm):

    
    name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Enter client name'
        }),
        help_text="Client name"
    )

    class Meta:
        model = Client
        fields = ['name']

    def clean_name(self):
        """Validate that name is not empty and has valid characters"""
        name = self.cleaned_data.get('name')
        
        if not name or name.strip() == '':
            raise ValidationError("Client name is required.")
        
        if len(name) < 2:
            raise ValidationError("Client name must be at least 2 characters long.")
        
        return name.strip()



