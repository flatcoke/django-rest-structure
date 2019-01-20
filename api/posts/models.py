from django.contrib.contenttypes.fields import GenericForeignKey, \
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models as m
from django.utils.translation import ugettext_lazy as _


class Flog(m.Model):
    id = m.AutoField(primary_key=True)
    user = m.ForeignKey('users.User', on_delete=m.CASCADE, related_name="flogs")
    title = m.CharField(_('title'), null=False, max_length=255)
    content = m.TextField(_('content'), null=True)

    created_at = m.DateTimeField(_('created'), auto_now_add=True, null=False)
    updated_at = m.DateTimeField(auto_now=True, null=False)

    comments = GenericRelation('Comment', object_id_field='post_id',
                               content_type_field='post_type')

    class Meta:
        verbose_name = _('flog')
        verbose_name_plural = _('flogs')
        db_table = 'flogs'
        ordering = ['-id']
        indexes = [
            m.Index(fields=['created_at'], name='idx_flogs_created_at'),
        ]


class Flatgram(m.Model):
    id = m.AutoField(primary_key=True)
    user = m.ForeignKey('users.User', related_name="flatgrams",
                        on_delete=m.CASCADE, )
    title = m.CharField(_('title'), null=False, max_length=255)
    content = m.TextField(_('content'), null=True)

    created_at = m.DateTimeField(_('created'), auto_now_add=True, null=False)
    updated_at = m.DateTimeField(auto_now=True, null=False)

    comments = GenericRelation('Comment', object_id_field='post_id',
                               content_type_field='post_type')

    class Meta:
        verbose_name = _('flatgram')
        verbose_name_plural = _('flatgrams')
        db_table = 'flatgrams'
        ordering = ['-id']
        indexes = [
            m.Index(fields=['created_at'], name='idx_flatgrams_created_at'),
        ]


class Comment(m.Model):
    id = m.AutoField(primary_key=True)
    user = m.ForeignKey('users.User', related_name="comments",
                        on_delete=m.CASCADE, )
    comment = m.ForeignKey('Comment', on_delete=m.CASCADE, blank=True,
                           null=True, related_name="comments")
    content = m.TextField(_('content'), null=False)

    post_type = m.ForeignKey(ContentType, on_delete=m.CASCADE)
    post_id = m.PositiveIntegerField()
    post = GenericForeignKey('post_type', 'post_id')

    created_at = m.DateTimeField(_('created'), auto_now_add=True, null=False)
    updated_at = m.DateTimeField(auto_now=True, null=False)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        db_table = 'comments'
        ordering = ['id']
        indexes = [
            m.Index(fields=['created_at'], name='idx_comments_created_at'),
        ]
