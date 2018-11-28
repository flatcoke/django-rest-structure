# -*- coding: utf-8 -*-
"""
api.users.models
~~~~~~~~~~~~~~~~
This module implements users basic information.
"""
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager as SuperUserManager)
from django.core.mail import send_mail
from django.db import models as m
from django.utils.translation import ugettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook

from api.models import SoftDeletionManager, SoftDeletionModel


class UserScopeMixin(object):
    @property
    def only_staff(self):
        return self.filter(is_staff=True)


class UserManager(SoftDeletionManager, SuperUserManager, UserScopeMixin):
    def __init__(self, *args, **kwargs):
        super(UserManager, self).__init__(*args, **kwargs)


class User(LifecycleModelMixin,
           AbstractBaseUser,
           SoftDeletionModel,
           PermissionsMixin):
    """
    Users within the Django authentication system are represented by this
    model.
    Email and password are required. Other fields are optional.
    """
    id = m.AutoField(primary_key=True)
    username = m.CharField(_('username'), unique=True, max_length=30)
    email = m.EmailField(_('email address'), unique=True, max_length=254)
    password = m.CharField(_('password'), max_length=128)
    is_staff = m.BooleanField(_('staff status'), default=False, )
    is_active = m.BooleanField(_('active'), default=True, )
    is_superuser = m.BooleanField(_('superuser'), default=False, )
    last_login_at = m.DateTimeField(_('last login'), blank=True, null=True)
    current_login_at = m.DateTimeField(
        _('current login'), blank=True, null=True)
    deleted_at = m.DateTimeField(_('deleted_at'), default=None,
                                 blank=True, null=True)
    created_at = m.DateTimeField(_('created_at'), auto_now_add=True,
                                 null=False)
    updated_at = m.DateTimeField(auto_now=True, null=False)

    objects = UserManager(only_alive=True)  # for soft delete

    last_login = None
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

        ordering = ['-id']

        indexes = [
            m.Index(fields=['created_at'], name='idx_users_created_at'),
        ]

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.email

    @hook('before_update', when='password', has_changed=True)
    @hook('before_create')
    def set_hashed_password(self):
        self.set_password(self.password)
