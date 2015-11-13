# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20151112_2039'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pageplugin',
            unique_together=set([('title', 'project')]),
        ),
        migrations.AlterIndexTogether(
            name='pageplugin',
            index_together=set([('title', 'project')]),
        ),
    ]
