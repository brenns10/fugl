# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20151112_2035'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('title', 'owner')]),
        ),
        migrations.AlterIndexTogether(
            name='project',
            index_together=set([('title', 'owner')]),
        ),
    ]
