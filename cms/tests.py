from django.test import TestCase
from django.urls import reverse

from cms.models import Place


class ListViewTest(TestCase):
    def test_correct_template(self):
        url = reverse('cms:place_list')
        response = self.client.get(url)
        self.assertTemplateUsed('cms/place_list')


class CreateViewTest(TestCase):
    def setUp(self):
        self.url = reverse('cms:place_create')
        self.price = 10000
        self.size = 80
        self.details = 'This is an amazing place'
        self.data = dict(details=self.details,
                         size=self.size,
                         price=self.price)

    def test_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cms/place_form.html')

    def test_form_in_context(self):
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        form = response.context['form']
        fields = ('details', 'size', 'price')
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
