from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from data.behaviours import TimeStampable
from data.models import Ingredient, Microorganism, Plant, Substance


class ErrorReport(TimeStampable):
    class Meta:
        verbose_name = "signalement d'erreur"
        verbose_name_plural = "signalements d'erreur"
        ordering = ["-creation_date"]

    class Status(models.TextChoices):
        NEW = "NEW", "Nouveau"
        ONGOING = "ONGOING", "En cours d'analyse"
        DONE = "DONE", "Traité"

    email = models.EmailField(_("email address"), blank=True)
    message = models.TextField("problème constaté", blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="auteur",
        related_name="error_reports",
    )

    status = models.TextField("statut", blank=True, choices=Status, default=Status.NEW)

    plant = models.ForeignKey(
        Plant,
        null=True,
        blank=True,
        related_name="error_reports",
        verbose_name="plante concernée",
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        null=True,
        blank=True,
        related_name="error_reports",
        verbose_name="ingredient concerné",
        on_delete=models.CASCADE,
    )
    microorganism = models.ForeignKey(
        Microorganism,
        null=True,
        blank=True,
        related_name="error_reports",
        verbose_name="micro-organisme concerné",
        on_delete=models.CASCADE,
    )
    substance = models.ForeignKey(
        Substance,
        null=True,
        blank=True,
        related_name="error_reports",
        verbose_name="substance concernée",
        on_delete=models.CASCADE,
    )

    @property
    def element_string(self):
        element = self.plant or self.ingredient or self.microorganism or self.substance
        if element:
            return f"{str(element)} (Type: {element._meta.verbose_name}, ID: {element.id})"
        return "ingrédient inconnu"
