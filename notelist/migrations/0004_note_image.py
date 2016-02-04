# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import notelist.models


class Migration(migrations.Migration):

    dependencies = [
        ('notelist', '0003_auto_20160202_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='image',
            field=models.ImageField(null=True, upload_to=notelist.models.image_directory_path, blank=True),
        ),
    ]
