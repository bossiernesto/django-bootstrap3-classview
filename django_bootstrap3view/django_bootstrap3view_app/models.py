from django.db import models
import datetime


class BaseEntity(models.Model):
    """Base Entity class.

    This class is used as a base class for the models defined in the created project. This class inherits from
    the models.Model class from django. By default this class adds the created_at and updated_at columns to the model
    class that extends from this class.

    .. note::

       This class can be expanded with behaviour commonly used in a model and that hasn't been implemented on it's base
       class.
    """
    NOT_IN_FIELDS = []

    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        now = datetime.datetime.now()
        kwargs.update(created_at=now, updated_at=now)
        models.Model.__init__(self, *args, **kwargs)

    def fields(self):
        """Method that returns a list of fields excepting the private attributes (starting with _).

        Args:
            none.

        returns:
            A list of attributes on the current model class.

        """
        return [key for key in self.__dict__.keys() if not key.startswith("_")]

    def update_fields(self):
        """Method that returns a list of fields excepting the private attributes and the ones defined on NOT_IN_FIELDS
        (by default this last list is empty).

        Args:
            none.

        returns:
            A list of attributes on the current model class excepting the private attributes and defined in
            NOT_IN_FIELDS.
        """
        return [field for field in self.fields() if field not in self.NOT_IN_FIELDS]

    class Meta:
        abstract = True