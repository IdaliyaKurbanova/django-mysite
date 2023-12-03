from django import forms
from .models import Product, Order, User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "description", "price", "discount",


class OrderForm(forms.Form):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())
    promocode = forms.CharField(max_length=100, required=False)
    user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None)
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={"cols": 40, "rows": 4}))
