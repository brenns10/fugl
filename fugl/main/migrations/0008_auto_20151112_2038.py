# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20151112_2037'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('title', 'project')]),
        ),
        migrations.AlterIndexTogether(
            name='tag',
            index_together=set([('title', 'project')]),
        ),
    ]
