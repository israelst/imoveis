import os
from unittest import TestCase, mock
from unittest.mock import Mock, patch

from django.forms.models import model_to_dict

from model_mommy.recipe import Recipe

from cms.forms import PlaceForm


class PlaceFormTest(TestCase):
    def setUp(self):
        self.place = Recipe('Place', _create_files=True)
        data = model_to_dict(self.place.make())
        picture = data.pop('picture')
        files = dict(picture=picture)
        self.data = data
        self.files = files

    def _test_correct_model(self):
        model = PlaceForm.Meta.model
        self.assertEqual('Place', (model))

    def test_fields(self):
        fields = ('picture',
                  'details',
                  'size',
                  'price',
                  'address',
                  'location',
        )
        self.assertSequenceEqual(fields, list(PlaceForm().fields.keys()))

    @patch('cms.forms.address_to_point')
    def test_invalid_address(self, address_to_point):
        address_to_point.side_effect = ValueError
        self.data['address'] = 'Invalid address'
        form = PlaceForm(data=self.data, files=self.files)
        self.assertFalse(form.is_valid())

    @patch('cms.forms.address_to_point')
    def test_valid_address(self, address_to_point):
        latlng = (-42, -24)
        address_to_point.return_value = latlng
        self.data['address'] = 'Avenida Rio Branco 1, Centro, Rio de Janeiro'
        form = PlaceForm(data=self.data, files=self.files)
        self.assertTrue(form.is_valid())
        place = form.save()
        self.assertEqual(latlng, place.location.coords)

    @patch('cms.forms.address_to_point')
    def test_location_is_not_required(self, address_to_point):
        latlng = (-42, -24)
        address_to_point.return_value = latlng
        form = PlaceForm(data=self.data, files=self.files)
        self.assertTrue(form.is_valid())
        place = form.save()
        self.assertEqual(latlng, place.location.coords)

    @patch('cms.forms.address_to_point')
    def test_ignore_informed_location(self, address_to_point):
        informed_latlng = 'POINT(-13 -17)'
        latlng = (-42, -24)
        address_to_point.return_value = latlng
        self.data['location'] = informed_latlng
        form = PlaceForm(data=self.data, files=self.files)
        self.assertTrue(form.is_valid())
        place = form.save()
        self.assertEqual(latlng, place.location.coords)
