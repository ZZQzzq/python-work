# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-02 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20170423_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='\u662f\u5426\u8f6e\u64ad'),
        ),
    ]