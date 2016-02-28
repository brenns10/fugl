# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20151130_1200'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name='post',
            index_together=set([]),
        ),
    ]
