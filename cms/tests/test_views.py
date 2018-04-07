import os
from unittest.mock import patch

from django.contrib.gis.geos import Point
from django.test import TestCase
from django.urls import reverse

from model_mommy.mommy import make
from model_mommy.recipe import Recipe

from cms.models import Place


class ListViewTest(TestCase):
    def test_correct_template(self):
        url = reverse('cms:place_list')
        response = self.client.get(url)
        self.assertTemplateUsed('cms/place_list')


class PlaceDetailViewTest(TestCase):
    def setUp(self):
        self.place = make(Place, _create_files=True)
        url = self.place.get_absolute_url()
        self.response = self.client.get(url)

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, 'cms/place_detail.html')

    def test_in_context(self):
        self.assertIn('object', self.response.context)
        obj = self.response.context['object']
        self.assertEqual(self.place, obj)


class PlaceListViewTest(TestCase):
    def setUp(self):
        self.url = reverse('cms:place_list')
        self.place = Recipe(Place, _create_files=True)

    def test_correct_template(self):
        place = self.place.make()
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cms/place_list.html')

    def test_context(self):
        place_1 = self.place.make()
        place_2 = self.place.make()
        response = self.client.get(self.url)
        self.assertIn('object_list', response.context)
        objs = response.context['object_list']
        self.assertCountEqual([place_1, place_2], objs)

    def test_empty_state(self):
        self.assertEqual(0, Place.objects.count())
        response = self.client.get(self.url)
        self.assertIn('object_list', response.context)
        objs = response.context['object_list']
        self.assertCountEqual([], objs)

    def test_order_by_distance_to_madureira(self):
        Botafogo = Point(-22.9577904, -43.1848308, srid=32140)
        Flamengo = Point(-22.9352825, -43.1805203, srid=32140)
        Centro = Point(-22.9058558, -43.1811104, srid=32140)
        madureira = dict(lat=-22.8716467, lng=-43.3391176)

        place_1 = self.place.make(location=Flamengo, details='Flamengo')
        place_2 = self.place.make(location=Botafogo, details='Botafogo')
        place_3 = self.place.make(location=Centro, details='Centro')

        response = self.client.get(self.url, data=madureira)
        self.assertIn('object_list', response.context)
        objs = response.context['object_list'].values_list('details', flat=True)
        self.assertSequenceEqual(['Centro', 'Flamengo', 'Botafogo'], objs)

    def test_order_by_distance_to_centro(self):
        Botafogo = Point(-22.9577904, -43.1848308, srid=32140)
        Flamengo = Point(-22.9352825, -43.1805203, srid=32140)
        Madureira = Point(-22.8716467, -43.3391176, srid=32140)
        centro = dict(lat=-22.9058558, lng=-43.1811104)

        place_1 = self.place.make(location=Flamengo, details='Flamengo')
        place_2 = self.place.make(location=Botafogo, details='Botafogo')
        place_3 = self.place.make(location=Madureira, details='Madureira')

        response = self.client.get(self.url, data=centro)
        self.assertIn('object_list', response.context)
        objs = response.context['object_list'].values_list('details', flat=True)
        self.assertSequenceEqual(['Flamengo', 'Botafogo', 'Madureira'], objs)


class CreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('cms:place_create')
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        picture_path = os.path.join(BASE_DIR, 'picture-fixture.jpg')
        self.picture = open(picture_path, 'rb')
        self.price = 10000
        self.size = 80
        self.details = 'This is an amazing place'
        self.address = 'Avenida Rio Branco 1, Centro, Rio de Janeiro'
        self.data = dict(address=self.address,
                         picture=self.picture,
                         details=self.details,
                         size=self.size,
                         price=self.price)

    @patch('cms.forms.address_to_point', return_value=(42, 42))
    def test_correct_template(self, address_to_point):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cms/place_form.html')

    @patch('cms.forms.address_to_point', return_value=(42, 42))
    def test_form_in_context(self, address_to_point):
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        form = response.context['form']
        fields = ('picture', 'address', 'details', 'size', 'price', 'location')
        self.assertCountEqual(fields, form.fields.keys())

    @patch('cms.forms.address_to_point', return_value=(42, 42))
    def test_redirect_after_created(self, address_to_point):
        self.assertEqual(0, Place.objects.count())
        response = self.client.post(self.url, self.data)
        self.assertEqual(1, Place.objects.count())
        place_id = str(Place.objects.first().id)
        url = reverse('cms:place_detail', args=[place_id])
        self.assertRedirects(response, url)

    @patch('cms.forms.address_to_point')
    def test_save(self, address_to_point):
        latlng = (-42, -24)
        address_to_point.return_value = latlng
        self.assertEqual(0, Place.objects.count())
        self.client.post(self.url, self.data)
        self.assertEqual(1, Place.objects.count())
        place = Place.objects.first()
        self.assertEqual(self.details, place.details)
        self.assertEqual(self.address, place.address)
        self.assertEqual(self.size, place.size)
        self.assertEqual(self.price, place.price)
        self.assertEqual(latlng, place.location.coords)
