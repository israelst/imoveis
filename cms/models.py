from django.db import models
from django.urls import reverse


class Place(models.Model):
    picture = models.ImageField(upload_to='images')
    details = models.TextField()
    size = models.DecimalField(max_digits=9, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def get_absolute_url(self):
        return reverse('cms:place_detail', args=[str(self.id)])
