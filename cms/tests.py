import os

from django.test import TestCase
from django.urls import reverse

from model_mommy.mommy import make

from cms.models import Place


class ListViewTest(TestCase):
    def test_correct_template(self):
        url = reverse('cms:place_list')
        response = self.client.get(url)
        self.assertTemplateUsed('cms/place_list')


class PlaceDetailViewTest(TestCase):
    def setUp(self):
        self.place = make(Place)
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

    def test_correct_template(self):
        place = make(Place)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cms/place_list.html')

    def test_context(self):
        place_1 = make(Place)
        place_2 = make(Place)
        response = self.client.get(self.url)
        self.assertIn('object_list', response.context)
        objs = response.context['object_list']
        self.assertCountEqual([place_1, place_2], objs)


class CreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('cms:place_create')
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        picture_path = os.path.join(BASE_DIR, 'picture-fixture.jpg')
        self.picture = open(picture_path, 'rb')
        self.price = 10000
        self.size = 80
        self.details = 'This is an amazing place'
        self.data = dict(picture=self.picture,
                         details=self.details,
                         size=self.size,
                         price=self.price)

    def test_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cms/place_form.html')

    def test_form_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        form = response.context['form']
        fields = ('picture', 'details', 'size', 'price')
        self.assertCountEqual(fields, form.fields.keys())

    def test_redirect_after_created(self):
        self.assertEqual(0, Place.objects.count())
        response = self.client.post(self.url, self.data)
        self.assertEqual(1, Place.objects.count())
        place_id = str(Place.objects.first().id)
        url = reverse('cms:place_detail', args=[place_id])
        self.assertRedirects(response, url)

    def test_save(self):
        self.assertEqual(0, Place.objects.count())
        self.client.post(self.url, self.data)
        self.assertEqual(1, Place.objects.count())
        place = Place.objects.first()
        self.assertEqual(self.details, place.details)
        self.assertEqual(self.size, place.size)
        self.assertEqual(self.price, place.price)
