# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-22 06:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0009_sumattr'),
    ]

    operations = [
        migrations.CreateModel(
            name='SumPageTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('title_text', models.CharField(max_length=256)),
            ],
        ),
    ]