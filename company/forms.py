from django import forms
from .models import Company, Contact
from django.forms.models import inlineformset_factory
from phonenumber_field.formfields import PhoneNumberField

class CompanyForm(forms.Form):
    name = forms.CharField(label='Company Name')
    address = forms.CharField(label="Company Address")
    contract_choices = (
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    )
    contract = forms.ChoiceField(choices = contract_choices )
    email = forms.EmailField(required=False)
    phone = PhoneNumberField(label='company Phone', required=False)

ModuleFormSet = inlineformset_factory(Company, Contact, fields=['email', 'phone'], can_delete=True)

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('email', 'phone')
    