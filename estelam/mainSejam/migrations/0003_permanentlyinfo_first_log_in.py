# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-13 05:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainSejam', '0002_temporaryinfo_first_log_in'),
    ]

    operations = [
        migrations.AddField(
            model_name='permanentlyinfo',
            name='first_log_in',
            field=models.BooleanField(default=False),
        ),
    ]
