from django.db import models

class Slidekeyterm(models.Model):
    title = models.CharField(max_length=256)
    keyterm = models.CharField(max_length=256)

class KeytermRelation(models.Model):
    k1 = models.CharField(max_length=256)
    k2 = models.CharField(max_length=256)

class Slide(models.Model):
    chapter = models.DecimalField(max_digits=10, decimal_places=0)
    subchapter = models.DecimalField(max_digits=10, decimal_places=0)
    page = models.DecimalField(max_digits=10, decimal_places=0)
