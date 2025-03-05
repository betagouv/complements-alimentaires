from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import DeclaredPlant, DeclaredMicroorganism, DeclaredSubstance, DeclaredIngredient


def generic_update_first_declaration(ingredient, declaration):
    if not ingredient or not declaration or ingredient.siccrf_id or ingredient.first_declaration:
        return
    ingredient.first_declaration = declaration


@receiver(pre_save, sender=DeclaredPlant)
def declared_plant_update_first_declaration(sender, instance, **kwargs):
    generic_update_first_declaration(instance.plant, instance.declaration)


@receiver(pre_save, sender=DeclaredMicroorganism)
def declared_microorganism_update_first_declaration(sender, instance, **kwargs):
    generic_update_first_declaration(instance.microorganism, instance.declaration)


@receiver(pre_save, sender=DeclaredSubstance)
def declared_substance_update_first_declaration(sender, instance, **kwargs):
    generic_update_first_declaration(instance.substance, instance.declaration)


@receiver(pre_save, sender=DeclaredIngredient)
def declared_ingredient_update_first_declaration(sender, instance, **kwargs):
    generic_update_first_declaration(instance.ingredient, instance.declaration)
