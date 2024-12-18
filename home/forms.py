# forms.py
from django import forms
from .models import Warranty, Vendor

class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = ['vendor', 'full_name', 'email', 'phone', 'model', 'date_of_sale', 'serial_number']

    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), required=True,empty_label="Select a Vendor")