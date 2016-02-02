# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('notelist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='text',
            field=models.TextField(verbose_name='text field', validators=[django.core.validators.MinLengthValidator(10, message='Do not allowed to post note shorter that 10 symbols.')]),
        ),
    ]
