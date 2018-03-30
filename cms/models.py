from django.db import models

class Place(models.Model):
    details = models.TextField()
    size = models.DecimalField(max_digits=9, decimal_places=2)
    price = models.DecimalField(max_digits=15, decimal_places=2)
