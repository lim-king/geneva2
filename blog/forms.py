# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms

from blog.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'photo_thumbnail', )
