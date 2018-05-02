# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-24 07:11
from __future__ import unicode_literals

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo_thumbnail',
            field=imagekit.models.fields.ProcessedImageField(default=1, upload_to='blog/post'),
            preserve_default=False,
        ),
    ]