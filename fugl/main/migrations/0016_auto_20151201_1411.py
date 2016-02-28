# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20151130_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectplugin',
            name='markup',
            field=models.TextField(max_length=5000),
        ),
    ]
