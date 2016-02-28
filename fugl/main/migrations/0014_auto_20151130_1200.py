# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20151128_1646'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name='page',
            index_together=set([]),
        ),
    ]
