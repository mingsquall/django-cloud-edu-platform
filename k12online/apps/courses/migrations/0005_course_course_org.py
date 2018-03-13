# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-12 00:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_auto_20180311_1758'),
        ('courses', '0004_auto_20180308_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.School', verbose_name='\u6240\u5c5e\u5b66\u6821'),
        ),
    ]
