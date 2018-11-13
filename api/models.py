from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token as Tk


# Create your models here.

class Token(Tk):
    created = None
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True,
                                      null=False)

    class Meta:
        verbose_name = _('auth_token')
        verbose_name_plural = _('auth_tokens')
        db_table = 'auth_tokens'
