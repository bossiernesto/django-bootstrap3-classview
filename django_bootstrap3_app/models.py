from django.db import models
import datetime


class BaseEntity(models.Model):
    NOT_IN_FIELDS = []

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        now = datetime.now()
        kwargs.update(created_at=now, updated_at=now)
        models.Model.__init__(self, *args, **kwargs)

    def fields(self):
        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    def update_fields(self):
        return [field for field in self.fields() if field not in self.NOT_IN_FIELDS]

    class Meta:
        abstract = True