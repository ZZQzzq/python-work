# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-23 13:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20170420_2222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviecomments',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie', verbose_name='\u7535\u5f71'),
        ),
    ]
