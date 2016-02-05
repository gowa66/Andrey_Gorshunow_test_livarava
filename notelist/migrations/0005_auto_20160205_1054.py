# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notelist', '0004_note_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='NoteBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('book', models.ForeignKey(to='notelist.Book')),
                ('note', models.ForeignKey(to='notelist.Note')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='notes',
            field=models.ManyToManyField(to='notelist.Note', through='notelist.NoteBook'),
        ),
    ]
