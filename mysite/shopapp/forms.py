from django import forms
from .models import Product, Order, User


class CSVFileForm(forms.Form):
    csv_file = forms.FileField()


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "description", "price", "discount", "archived"

    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected':True}), required=False)

# class OrderForm(forms.Form):
#     products = forms.ModelMultipleChoiceField(queryset=Product.objects.all())
#     promocode = forms.CharField(max_length=100, required=False)
#     user = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None)
#     delivery_address = forms.CharField(widget=forms.Textarea(attrs={"cols": 40, "rows": 4}))


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"
