# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin, messages
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from management.models import User, MainTimeBoard
from management.forms import SetCertificationDateForm
from blog.models import Post

import datetime


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'nickname')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'is_admin', 'profile_image')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'permission', 'is_certificated', 'certification_date',
                    'nickname', 'post_count')
    # list_filter = ('is_admin',)
    list_filter = ('is_active', 'permission')
    list_editable = ('permission',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    actions = ['set_certification_date']
    action_form = SetCertificationDateForm

    def post_count(self, obj):
        return Post.objects.filter(author_id=obj.id).count()

    def set_certification_date(self, request, queryset):
        year = request.POST.get('certification_date_year')
        month = request.POST.get('certification_date_month')
        day = request.POST.get('certification_date_day')

        if year and month and day:
            date_str = '{0}-{1}-{2}'.format(year, month, day)
            date = datetime.datetime.strptime(date_str, "%Y-%d-%m").date()

            for member in queryset:
                User.objects.filter(id=member.id).update(is_certificated=True, certification_date=date)

            messages.success(request, '{0}명의 회원을 인증했습니다.'.format(len(queryset)))
        else:
            messages.error(request, '날짜가 선택되지 않았습니다.')

    post_count.short_description = '작성한 글 수'
    set_certification_date.short_description = '선택된 유저를 해당 날짜 기준으로 인증합니다.'
# Now register the new UserAdmin...


admin.site.register(User, UserAdmin)
admin.site.register(MainTimeBoard)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
