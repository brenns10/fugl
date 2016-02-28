# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import main.models.project


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20151201_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(validators=[main.models.project.validate_project], help_text='Required. Letters, digits, and -/_.', max_length=50),
        ),
    ]
