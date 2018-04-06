from django import forms
from django.contrib.gis.geos import Point

from cms.models import Place
from cms.services import address_to_point


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        address = cleaned_data.get('address')

        try:
            _location = address_to_point(address)
            location = Point(*_location)
            self.cleaned_data['location'] = location
        except Exception as e:
            self.add_error('address', str(e))
