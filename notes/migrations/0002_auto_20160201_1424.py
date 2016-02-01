# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={},
        ),
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.CharField(max_length=200),
        ),
    ]
