from django import forms
import datetime

class FilterForm(forms.Form):
    title = forms.CharField(label='Title', max_length=30)
    logo_url = forms.CharField(max_length=250)
    description = forms.CharField(max_length=500, widget=forms.Textarea)
    site = forms.ChoiceField(choices=(('ebay.co.uk','ebay.co.uk'),('ebay.com','ebay.com')))
    search_text = forms.CharField(max_length=100)



    category = forms.ChoiceField(choices=(('12576','Bussiness & Industrial'),('15032','Cell Phones & Accessories'),('58058','Computers/Tablets & Networking')))

    # Condition check boxes:
    cond_new = forms.BooleanField(label='New', required=False)
    cond_new_other = forms.BooleanField(label='New other', required=False)
    cond_manufacturer_refurbished = forms.BooleanField(label='Manufacturer refurbished', required=False)
    cond_seller_refurbished = forms.BooleanField(label='Seller refurbished', required=False)
    cond_used = forms.BooleanField(label='Used', required=False)
    cond_for_parts = forms.BooleanField(label='For parts or not working', required=False)
    cond_not_specified = forms.BooleanField(label='Not specified', required=False)

    min_price = forms.FloatField()
    max_price = forms.FloatField()


