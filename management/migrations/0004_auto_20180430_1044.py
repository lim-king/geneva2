# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-30 01:44
from __future__ import unicode_literals

import blog.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_maintimeboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintimeboard',
            name='text',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='maintimeboard',
            name='photo_thumbnail',
            field=blog.fields.ThumbnailImageField(upload_to='static/timeboard/%Y/%m'),
        ),
    ]