# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-03 16:39
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpaotu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportSamplesMissingMetadataLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('samples_without_metadata', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
            ],
        ),
    ]
