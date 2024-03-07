from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


class Company(models.Model):
    class Meta:
        verbose_name = "entreprise"

    social_name = models.CharField("dénomination sociale")
    commercial_name = models.CharField("enseigne", help_text="nom commercial")
    siret = models.CharField(
        "n° SIRET", help_text="14 chiffres", validators=[MinLengthValidator(14), MaxLengthValidator(14)]
    )

    def __str__(self):
        return self.social_name
