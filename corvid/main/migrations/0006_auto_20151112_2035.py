# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20151112_2034'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('title', 'project')]),
        ),
        migrations.AlterIndexTogether(
            name='post',
            index_together=set([('title', 'project')]),
        ),
    ]
