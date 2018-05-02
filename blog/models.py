# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.forms import Media
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail
from blog.fields import ThumbnailImageField


class Post(models.Model):
    author = models.ForeignKey('management.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    photo_thumbnail = ThumbnailImageField(upload_to='static/blog/post/%Y/%m')
    active = models.BooleanField(
            null=False, default=True
    )
    # photo_thumbnail = ProcessedImageField(
    #     upload_to='static/blog/post',
    #     processors=[Thumbnail(652, 400)],  # 처리할 작업 목룍
    #     format='JPEG',  # 최종 저장 포맷
    #     options={'quality': 60})  # 저장 옵션

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
