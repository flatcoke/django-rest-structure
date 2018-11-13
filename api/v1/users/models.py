# -*- coding: utf-8 -*-
"""
api.users.models
~~~~~~~~~~~~~~~~
This module implements users basic information.
"""
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        BaseUserManager)

# from rest_framework.authtoken.models import Token
from api.models import Token
from flatcoke.settings import AUTH_USER_MODEL


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=UserManager.normalize_email(email),
            is_staff=False, is_active=True, is_superuser=False,
            created_at=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    """
    Users within the Django authentication system are represented by this
    model.
    Email and password are required. Other fields are optional.
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(_('username'), unique=True, max_length=30)
    email = models.EmailField(_('email address'), unique=True, max_length=254)
    password = models.CharField(_('password'), max_length=128)
    is_staff = models.BooleanField(_('staff status'), default=False, )
    is_active = models.BooleanField(_('active'), default=True, )
    is_superuser = models.BooleanField(_('superuser'), default=False, )
    last_login_at = models.DateTimeField(_('last login'), blank=True, null=True)
    current_login_at = models.DateTimeField(
        _('current login'), blank=True, null=True)
    created_at = models.DateTimeField(_('date joined'), auto_now_add=True,
                                      null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    objects = UserManager()

    last_login = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

        indexes = [
            models.Index(fields=['created_at'], name='users.created_at'),
        ]

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.email


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
