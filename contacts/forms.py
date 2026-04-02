
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'surname', 'email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name',
            }),
            'surname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter surname',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise forms.ValidationError('First name is required.')
        return name

    def clean_surname(self):
        surname = self.cleaned_data.get('surname', '').strip()
        if not surname:
            raise forms.ValidationError('Surname is required.')
        return surname

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise forms.ValidationError('Email address is required.')
        qs = Contact.objects.filter(email=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError('A contact with this email address already exists.')
        return email