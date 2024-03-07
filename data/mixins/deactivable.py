from django.db import models


class DeactivableQuerySet(models.query.QuerySet):
    class Meta:
        abstract = True

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)


class Deactivable(models.Model):
    """Used when an item can be deactivated, then reactivated."""

    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True)

    def invert_activity(self) -> bool:
        self.is_active = not self.is_active
        self.save()
        return self

    def activate(self):
        self.is_active = True
        self.save()

    def deactivate(self):
        self.is_active = False
        self.save()
