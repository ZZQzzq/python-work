# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-05-12 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_book_is_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookdetail',
            name='book_info',
            field=models.TextField(default='', verbose_name='\u56fe\u4e66\u4fe1\u606f'),
        ),
    ]
