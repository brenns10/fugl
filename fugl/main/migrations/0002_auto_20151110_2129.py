# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='content',
            field=models.TextField(max_length=50000),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=50000),
        ),
    ]
