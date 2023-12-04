from django.db import models


class Family(models.Model):
    class Meta:
        verbose_name = "Famille de plante"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)  # TODO : à vérifier une fois le CSV reçu
    name_en = models.CharField(max_length=200, blank=True)

    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class Plant(models.Model):
    class Meta:
        verbose_name = "Plante"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    family = models.ForeignKey(Family, on_delete=models.SET_NULL, verbose_name="Famille de plante")
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)
    public_comments = models.CharField(max_length=1000, null=True, blank=True, verbose_name="Commentaires publics")
    private_comments = models.CharField(max_length=2000, blank=True, verbose_name="Commentaires privés")

    # champs présents dans le CSV mais inutilisés
    # fctingr = models.IntegerField()
    # stingsbs = models.IntegerField()
    # commentaire_public_en = models.CharField(max_length=1000, blank=True)
    # commentaire_privé_en = models.CharField(max_length=2000, blank=True) # TODO : intégrer les quelques données ici
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class PlantSynonym(models.Model):
    class Meta:
        verbose_name = "Synonymes de plante"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()


class PlantPart(models.Model):
    class Meta:
        verbose_name = "Partie de plante"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, blank=True)

    # champs présents dans le CSV mais inutilisés
    # ordre = models.IntegerField()
    # obsolet = models.BooleanField()
