# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20151112_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
