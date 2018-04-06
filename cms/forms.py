from django import forms

from cms.models import Place
from cms.services import address_to_point


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        address = cleaned_data.get('address')
        location = cleaned_data.get('location')

        try:
            _location = address_to_point(address)
            location.coords = _location
            self.cleaned_data['location'] = location
        except Exception as e:
            self.add_error('address', e)
