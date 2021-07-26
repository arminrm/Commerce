from .models import Listing
from django.forms import ModelForm

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'current_price']
