from django.db import models

class Slide(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
