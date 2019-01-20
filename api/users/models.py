# -*- coding: utf-8 -*-
"""
api.users.models
~~~~~~~~~~~~~~~~
This module implements users basic information.
"""
import requests
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
                                        UserManager as SuperUserManager)
from django.core.mail import send_mail
from django.db import models as m
from django.utils.translation import ugettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook

from api.models import SoftDeletionManager, SoftDeletionModel
from api.users.exceptions import (InvalidFacebookTokenException,
                                  InvalidGoogleOauthTokenException)

VALID_FACEBOOK_TOKEN_URL = "https://graph.facebook.com/me"
VALID_GOOGLE_OAUTH2_TOKEN_URL = "https://www.googleapis.com/oauth2/v1/userinfo"


class UserScopeMixin(object):
    @property
    def only_staff(self):
        return self.filter(is_staff=True)


class UserManager(SoftDeletionManager, SuperUserManager, UserScopeMixin):
    def __init__(self, *args, **kwargs):
        super(UserManager, self).__init__(*args, **kwargs)

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, password=password,
                          **extra_fields)
        user.save(using=self._db)
        return user


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
    username = m.CharField(_('username'), max_length=30)
    email = m.EmailField(_('email address'), unique=True, max_length=100)
    password = m.CharField(_('password'), max_length=128)
    is_staff = m.BooleanField(_('staff status'), default=False, )
    is_active = m.BooleanField(_('active'), default=True, )
    is_superuser = m.BooleanField(_('superuser'), default=False, )
    last_login_at = m.DateTimeField(_('last login'), blank=True, null=True)
    current_login_at = m.DateTimeField(_('current login'), blank=True,
                                       null=True)
    provider = m.CharField(_('provider'), default='email', max_length=30)
    uid = m.CharField(_('uid'), default=None, max_length=255)

    deleted_at = m.DateTimeField(_('deleted_at'), default=None,
                                 blank=True, null=True)
    created_at = m.DateTimeField(_('created_at'), auto_now_add=True,
                                 null=False)
    updated_at = m.DateTimeField(auto_now=True, null=False)

    objects = UserManager(only_alive=True)  # for soft delete

    last_login = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

        ordering = ['-id']

        indexes = [
            m.Index(fields=['created_at'], name='idx_users_created_at'),
            m.Index(fields=['username'], name='idx_users_username'),
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

    @hook('before_create', when='provider', is_now='email')
    def set_uid_if_provider_is_email(self):
        """If provider is email set email to uid."""
        self.uid = self.email

    @classmethod
    def first_or_create_user_by_facebook_token(cls, facebook_token,
                                               fields=None):
        if fields is None:
            fields = ['email', 'name']
        params = {'access_token': facebook_token, 'fields': ','.join(fields)}
        res = requests.get(VALID_FACEBOOK_TOKEN_URL, params=params)
        if res.status_code != 200:
            raise InvalidFacebookTokenException()
        facebook_data = res.json()
        user = cls.objects.filter(provider='facebook',
                                  uid=facebook_data['id']).first()
        if user is not None:
            return user
        return cls.objects.create(
            provider='facebook',
            password=cls.objects.make_random_password(),
            email=facebook_data['email'],
            username=facebook_data['name'].replace(' ', ''),
            uid=facebook_data['id'])

    @classmethod
    def first_or_create_user_by_google_token(cls, google_token):
        res = requests.get(VALID_GOOGLE_OAUTH2_TOKEN_URL,
                           params={'access_token': google_token})
        if res.status_code != 200:
            raise InvalidGoogleOauthTokenException()
        google_oauth2_data = res.json()
        user = cls.objects.filter(provider='google_oauth2',
                                  uid=google_oauth2_data['id']).first()
        if user is not None:
            return user
        return cls.objects.create(
            provider='google_oauth2',
            password=cls.objects.make_random_password(),
            email=google_oauth2_data['email'],
            username=google_oauth2_data['name'].replace(' ', ''),
            uid=google_oauth2_data['id'])
