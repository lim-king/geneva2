# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db import models
from blog.fields import ThumbnailImageField


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            nickname=nickname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    TYPE_PERMISSIONS = (
        ('AT', '광고주'),
        ('MB', '일반'),
    )

    email = models.EmailField(verbose_name='이메일', max_length=255, unique=True,)
    nickname = models.CharField('닉네임', max_length=30)
    permission = models.CharField('권한', max_length=2, choices=TYPE_PERMISSIONS, default='MB')
    certification_date = models.DateField('인증일', default=None, null=True, blank=True)
    is_certificated = models.BooleanField('인증여부', default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    profile_image = ThumbnailImageField(upload_to='static/profile_image/%Y/%m')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class MainTimeBoard(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    photo_thumbnail = ThumbnailImageField(upload_to='static/timeboard/%Y/%m')
    active = models.BooleanField(
            null=False, default=True
    )
    # photo_thumbnail = ProcessedImageField(
    #     upload_to='static/blog/post',
    #     processors=[Thumbnail(652, 400)],  # 처리할 작업 목룍
    #     format='JPEG',  # 최종 저장 포맷
    #     options={'quality': 60})  # 저장 옵션

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
