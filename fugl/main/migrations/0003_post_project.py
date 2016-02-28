# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20151110_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='project',
            field=models.ForeignKey(to='main.Project', default=1),
            preserve_default=False,
        ),
    ]
