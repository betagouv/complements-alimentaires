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
