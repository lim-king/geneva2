# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.admin.helpers import ActionForm
from django.forms import SelectDateWidget
from management.models import User

import datetime


class SetCertificationDateForm(ActionForm):
    certification_date = forms.DateField(
        widget=SelectDateWidget,
        initial=(datetime.date.today())
    )


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'profile_image', )
