# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-18 13:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.BookKind', verbose_name='\u56fe\u4e66\u7c7b\u578b'),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_tag',
            field=models.CharField(choices=[('wx', '\u6587\u5b66'), ('wh', '\u6587\u5316'), ('kj', '\u79d1\u6280'), ('jg', '\u7ecf\u7ba1'), ('lx', '\u6d41\u884c'), ('sh', '\u751f\u6d3b')], default='wx', max_length=10, verbose_name='\u56fe\u4e66\u6807\u7b7e'),
        ),
    ]
