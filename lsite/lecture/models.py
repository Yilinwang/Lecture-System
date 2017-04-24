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
    video_title = models.CharField(max_length=256)
    title = models.CharField(max_length=256)

class SumPageTitle(models.Model):
    title = models.CharField(max_length=256)
    title_text = models.CharField(max_length=256)

class SumAttr(models.Model):
    title = models.CharField(max_length=256)
    time = models.CharField(max_length=256)
    brief_time = models.CharField(max_length=256)

class ChapVideoAttr(models.Model):
    title = models.CharField(max_length=256)
    time = models.CharField(max_length=256)
    chapter3time = models.CharField(max_length=256)
    chapter10time = models.CharField(max_length=256)

class VideoAttr(models.Model):
    title = models.CharField(max_length=256)
    prev_ch = models.DecimalField(max_digits=10, decimal_places=0)
    cur_ch = models.DecimalField(max_digits=10, decimal_places=0)
    ch_time = models.CharField(max_length=256)
    prev_subch = models.DecimalField(max_digits=10, decimal_places=0)
    cur_subch = models.DecimalField(max_digits=10, decimal_places=0)
    subch_time = models.CharField(max_length=256)
    prev = models.DecimalField(max_digits=10, decimal_places=0)
    cur = models.DecimalField(max_digits=10, decimal_places=0)
    time = models.CharField(max_length=256)
