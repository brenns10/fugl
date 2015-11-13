# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_post_project'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('title', 'project')]),
        ),
        migrations.AlterIndexTogether(
            name='category',
            index_together=set([('title', 'project')]),
        ),
    ]
