from django.forms import ModelForm
from .models import Listing 
class ImageForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["item", "descript", "category","file_path" ]
    