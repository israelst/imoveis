from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.urls import reverse


RJ = Point(-22.9013763,-43.1783903)


class Place(models.Model):
    picture = models.ImageField(upload_to='images')
    details = models.TextField()
    size = models.DecimalField(max_digits=9, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    location = models.PointField(default=RJ)

    def get_absolute_url(self):
        return reverse('cms:place_detail', args=[str(self.id)])
