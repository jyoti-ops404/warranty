# forms.py
from django import forms
from .models import Warranty, Vendor,ContactUs,Inquiry

class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = ['vendor', 'full_name', 'email', 'phone', 'model', 'date_of_sale', 'serial_number']

    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), required=True,empty_label="Select a Vendor")

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'message']

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'phone', 'email']