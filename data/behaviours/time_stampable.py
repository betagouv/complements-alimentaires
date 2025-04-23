import contextlib

from django.db import models


class TimeStampableQueryset(models.query.QuerySet):
    class Meta:
        abstract = True

    def created_between(self, i_start, i_end):
        """
        Returns all objects created between the provided interval
        """

        assert i_start <= i_end
        return self.filter(creation_date__lte=i_end, creation_date__gte=i_start)


class TimeStampable(models.Model):
    class Meta:
        abstract = True

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)


@contextlib.contextmanager
def suppress_autotime(model, fields):
    """
    Décorateur pour annuler temporairement le auto_now et auto_now_add de certains champs
    Copié depuis https://stackoverflow.com/questions/7499767/temporarily-disable-auto-now-auto-now-add
    """
    _original_values = {}
    for field in model._meta.local_fields:
        if field.name in fields:
            _original_values[field.name] = {
                "auto_now": field.auto_now,
                "auto_now_add": field.auto_now_add,
            }
            field.auto_now = False
            field.auto_now_add = False
    try:
        yield
    finally:
        for field in model._meta.local_fields:
            if field.name in fields:
                field.auto_now = _original_values[field.name]["auto_now"]
                field.auto_now_add = _original_values[field.name]["auto_now_add"]
