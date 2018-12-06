from django.db import models as m
from django.db.models.query import QuerySet
from django.utils import timezone
from django_lifecycle import LifecycleModelMixin


class Model(LifecycleModelMixin, m.Model):
    def delete(self):
        setattr(self, 'updated_at', timezone.now())
        self.save()

    class Meta:
        abstract = True


class SoftDeletionManager(m.Manager):
    def __init__(self, *args, **kwargs):
        self.only_alive = kwargs.pop('only_alive', False)
        self.only_deleted = kwargs.pop('only_deleted', False)

        if self.only_alive and self.only_deleted:
            raise ValueError()
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.only_alive:
            return SoftDeletionQuerySet(self.model).filter(
                deleted_at__isnull=True)
        elif self.only_deleted:
            return SoftDeletionQuerySet(self.model).filter(
                deleted_at__isnull=False)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(
            deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionModel(m.Model):
    deleted_at = m.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager(only_alive=True)
    only_deleted = SoftDeletionManager(only_deleted=True)
    with_deleted = SoftDeletionManager()

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()
