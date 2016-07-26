# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-14 19:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('MovieId', models.AutoField(primary_key=True, serialize=False)),
                ('MovieName', models.CharField(max_length=100)),
                ('Year', models.CharField(max_length=4)),
                ('ReleaseDate', models.DateField()),
                ('Horror', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Romantic', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Comedy', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Fantasy', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Dark', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Historic', models.DecimalField(decimal_places=2, max_digits=3)),
                ('ScienceFiction', models.DecimalField(decimal_places=2, max_digits=3)),
                ('SuperHero', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Drama', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Adult', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Animation', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Adventure', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Action', models.DecimalField(decimal_places=2, max_digits=3)),
                ('Stars', models.CharField(max_length=200)),
                ('Director', models.CharField(max_length=200)),
                ('IMDBRating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('AvgUsrRating', models.DecimalField(decimal_places=1, max_digits=3)),
                ('NoRating', models.IntegerField()),
                ('NoPredictions', models.IntegerField()),
                ('Keywords', models.CharField(max_length=1000, null=True)),
                ('Description', models.TextField(null=True)),
                ('Poster', models.URLField(null=True)),
                ('ImdbURL', models.URLField(unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='movies',
            unique_together=set([('MovieName', 'Year')]),
        ),
    ]