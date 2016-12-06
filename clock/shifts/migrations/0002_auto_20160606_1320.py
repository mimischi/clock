# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-06 13:20
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shifts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shift',
            options={'ordering': ['shift_finished']},
        ),
        migrations.AlterField(
            model_name='shift',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='contracts.Contract', verbose_name='Contract'),
        ),
    ]
