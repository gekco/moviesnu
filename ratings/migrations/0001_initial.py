# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 19:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rating', models.IntegerField(null=True)),
                ('PredictedRating', models.IntegerField(null=True)),
                ('Review', models.TextField(null=True)),
                ('MovieId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movies')),
                ('UserId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='ratings',
            unique_together=set([('UserId', 'MovieId')]),
        ),
    ]
