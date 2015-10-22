# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=50000)),
            ],
        ),
        migrations.CreateModel(
            name='PagePlugin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('head_markup', models.CharField(max_length=5000)),
                ('body_markup', models.CharField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=50000)),
                ('date_created', models.DateTimeField()),
                ('date_updated', models.DateTimeField()),
                ('category', models.ForeignKey(to='main.Category')),
                ('post_plugins', models.ManyToManyField(to='main.PagePlugin')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
                ('preview_url', models.URLField()),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectPlugin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('markup', models.CharField(max_length=5000)),
                ('project', models.ForeignKey(to='main.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('posts', models.ManyToManyField(to='main.Post')),
                ('project', models.ForeignKey(to='main.Project')),
            ],
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('filepath', models.FilePathField()),
                ('body_markup', models.CharField(max_length=5000)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='theme',
            field=models.ForeignKey(to='main.Theme'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='main.Tag'),
        ),
        migrations.AddField(
            model_name='pageplugin',
            name='project',
            field=models.ForeignKey(to='main.Project'),
        ),
        migrations.AddField(
            model_name='page',
            name='post_plugins',
            field=models.ManyToManyField(to='main.PagePlugin'),
        ),
        migrations.AddField(
            model_name='category',
            name='project',
            field=models.ForeignKey(to='main.Project'),
        ),
    ]
