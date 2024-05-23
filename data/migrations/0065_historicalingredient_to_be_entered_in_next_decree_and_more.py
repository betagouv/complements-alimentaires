# Modifié manuellement pour
# * set_default to_be_entered_in_next_decree à 1 pour les status siccrf à 3 - à inscrire

from django.db import migrations, models
from data.models import Ingredient, Plant, Microorganism, Substance


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0064_merge_20240509_1753"),
    ]
    
    def set_default(apps, schema_editor):
        for table in [Ingredient, Plant, Microorganism, Substance]:
            for obj in table.objects.all().iterator():
                obj.to_be_entered_in_next_decree = obj.status == 3
                if obj.status == 3:
                    obj.status = 1
                if obj.status == 4:
                    obj.status = None
                obj.save()

    def reverse_set_default(apps, schema_editor):
        pass

    operations = [
        migrations.AddField(
            model_name="historicalingredient",
            name="to_be_entered_in_next_decree",
            field=models.BooleanField(
                default=0,
                editable=False,
                verbose_name="L'ingrédient doit-il être inscrit dans le prochain décret ?",
            ),
        ),
        migrations.AddField(
            model_name="historicalmicroorganism",
            name="to_be_entered_in_next_decree",
            field=models.BooleanField(
                default=0,
                editable=False,
                verbose_name="L'ingrédient doit-il être inscrit dans le prochain décret ?",
            ),
        ),
        migrations.AddField(
            model_name="historicalplant",
            name="to_be_entered_in_next_decree",
            field=models.BooleanField(
                default=0,
                editable=False,
                verbose_name="L'ingrédient doit-il être inscrit dans le prochain décret ?",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubstance",
            name="to_be_entered_in_next_decree",
            field=models.BooleanField(
                default=0,
                editable=False,
                verbose_name="L'ingrédient doit-il être inscrit dans le prochain décret ?",
            ),
        ),
        migrations.AddField(
            model_name="ingredient",
            name="to_be_entered_in_next_decree",
            field=models.BooleanField(
                default=0,
                editable=False,
                verbose_name="L'ingrédient doit-il être inscrit dans le prochain décret ?",
            ),
        ),
        migrations.AddField(
            model_name="microorganism",
            name="to_be_entered_in_next_decree",
            field=models.BooleanField(
                default=0,
                editable=False,
                verbose_name="L'ingrédient doit-il être inscrit dans le prochain décret ?",
            ),
        ),
        migrations.AddField(
            model_name="plant",
            name="to_be_entered_in_next_decree",
            field=models.BooleanField(
                default=0,
                editable=False,
                verbose_name="L'ingrédient doit-il être inscrit dans le prochain décret ?",
            ),
        ),
        migrations.AddField(
            model_name="substance",
            name="to_be_entered_in_next_decree",
            field=models.BooleanField(
                default=0,
                editable=False,
                verbose_name="L'ingrédient doit-il être inscrit dans le prochain décret ?",
            ),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="status",
            field=models.IntegerField(
                choices=[(None, "inconnu"), (1, "autorisé"), (2, "non autorisé")],
                null=True,
                verbose_name="statut de l'ingrédient ou substance",
            ),
        ),
        migrations.AlterField(
            model_name="microorganism",
            name="status",
            field=models.IntegerField(
                choices=[(None, "inconnu"), (1, "autorisé"), (2, "non autorisé")],
                null=True,
                verbose_name="statut de l'ingrédient ou substance",
            ),
        ),
        migrations.AlterField(
            model_name="plant",
            name="status",
            field=models.IntegerField(
                choices=[(None, "inconnu"), (1, "autorisé"), (2, "non autorisé")],
                null=True,
                verbose_name="statut de l'ingrédient ou substance",
            ),
        ),
        migrations.AlterField(
            model_name="substance",
            name="status",
            field=models.IntegerField(
                choices=[(None, "inconnu"), (1, "autorisé"), (2, "non autorisé")],
                null=True,
                verbose_name="statut de l'ingrédient ou substance",
            ),
        ),
        migrations.RunPython(set_default, reverse_set_default),

    ]
