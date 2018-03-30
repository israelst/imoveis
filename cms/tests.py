from django.test import TestCase
from django.urls import reverse


class ListViewTest(TestCase):
    def test_correct_template(self):
        url = reverse('place_list')
        response = self.client.get(url)
        self.assertTemplateUsed('cms/place_list')
