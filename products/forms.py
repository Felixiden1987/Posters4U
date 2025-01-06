from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

class SortForm(forms.Form):
    SORT_OPTIONS = (
        ('None_None', 'Sort by...'),
        ('price_low_high', 'Price (low to high)'),
        ('price_high_low', 'Price (high to low)'),
        ('rating_low_high', 'Rating (low to high)'),
        ('rating_high_low', 'Rating (high to low)'),
        ('name_az', 'Name (A to Z)'),
        ('name_za', 'Name (Z to A)'),
    )

    sort = forms.ChoiceField(choices=SORT_OPTIONS, required=False)