from django.db import models


class Verifiable(models.Model):

    class Meta:
        abstract = True

    is_verified = models.BooleanField("Vérifié ?", default=False)

    def verify(self):
        self.is_verified = True
        self.save()

    def unverify(self):
        self.is_verified = False
        self.save()
