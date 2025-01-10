from django.db import models


class AutoValidable(models.Model):
    """
    Will force the validation process on save.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        * fields_with_no_validation est un set
        """
        fields_with_no_validation = kwargs.pop("fields_with_no_validation", ())
        if fields_with_no_validation:
            self.clean_fields(exclude=fields_with_no_validation)
            self.clean()
            self.validate_unique()
            self.validate_constraints()
        else:
            self.full_clean()
        super().save(*args, **kwargs)
