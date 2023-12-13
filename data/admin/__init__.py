from .user import UserAdmin  # noqa
from .blogpost import BlogPostAdmin  # noqa

from django.contrib import admin

from data.models import Ingredient, Plant, PlantPart, PlantFamily, Microorganism, Substance  # noqa

admin.site.register(Ingredient)
admin.site.register(Plant)
admin.site.register(PlantPart)
admin.site.register(PlantFamily)
admin.site.register(Microorganism)
admin.site.register(Substance)
