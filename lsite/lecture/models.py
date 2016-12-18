from django.db import models

class Slide(models.Model):
    title = models.CharField(max_length=256)
    keyterm = models.CharField(max_length=256)

class SIndex(models.Model):
    chapter = models.DecimalField(max_digits=10, decimal_places=0)
    index = models.DecimalField(max_digits=10, decimal_places=0)
