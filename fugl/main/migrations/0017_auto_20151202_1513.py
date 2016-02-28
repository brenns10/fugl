# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20151201_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pageplugin',
            name='body_markup',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='pageplugin',
            name='head_markup',
            field=models.TextField(max_length=5000),
        ),
    ]
