
from django import forms
from restaurent_manager.models import Product

class ImageForm(forms.ModelForm):
   class Meta:
      model=Product
      fields=['image']
    