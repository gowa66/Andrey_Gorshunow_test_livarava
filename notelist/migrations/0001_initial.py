# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import notelist.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='text field')),
                ('image', models.ImageField(null=True, upload_to=notelist.models.image_directory_path, blank=True)),
            ],
            options={
                'verbose_name_plural': 'text notes',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='notes',
            field=models.ManyToManyField(to='notelist.Note'),
        ),
    ]
