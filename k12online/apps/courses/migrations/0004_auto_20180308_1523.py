# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-08 15:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20180308_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='degree',
            field=models.CharField(choices=[('low', '\u521d\u7ea7'), ('mid', '\u4e2d\u7ea7'), ('high', '\u9ad8\u7ea7')], max_length=3, verbose_name='\u96be\u5ea6'),
        ),
    ]
