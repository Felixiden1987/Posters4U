from django import forms
from .models import Testimonial, Product


class TestimonialForm(forms.ModelForm):
    """Testimonial form allow user to
    give review about the product"""
    BANNED_KEYWORDS = [
        'disgusting', 'annoying', 'pathetic',
        'terrible', 'awful', 'horrible', 'ridiculous',
        'absurd', 'lame', 'trivial'
    ]

    class Meta:
        model = Testimonial
        fields = ['product', 'message']

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Product",
        widget=forms.Select(attrs={'class': 'border-line'})
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={'class': 'border-line'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError(
                "The message must be at least 10 characters long.")
        if len(message) > 500:
            raise forms.ValidationError(
                "The message cannot exceed 500 characters.")

        for word in self.BANNED_KEYWORDS:
            if word in message.lower():
                raise forms.ValidationError(
                    f"The message contains inappropriate content: '{word}'."
                    "Please remove offensive words."
                )
        return message
