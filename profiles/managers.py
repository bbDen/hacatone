from django.db.models import manager
from django.db.models.manager import Manager


class CommentManager(Manager):

    def all(self):
        return super().get_queryset().order_by('-sent_at')

    def filter(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).order_by('-sent_at')