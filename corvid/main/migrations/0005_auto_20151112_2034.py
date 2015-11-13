# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20151112_2025'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('title', 'project')]),
        ),
        migrations.AlterIndexTogether(
            name='page',
            index_together=set([('title', 'project')]),
        ),
    ]
