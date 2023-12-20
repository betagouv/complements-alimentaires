from django.contrib import admin

from .user import UserAdmin  # noqa
from .blogpost import BlogPostAdmin  # noqa
from .substance import SubstanceAdmin  # noqa

from data.models import Ingredient, Plant, PlantPart, Family, Microorganism  # noqa

admin.site.register(Ingredient)
admin.site.register(Plant)
admin.site.register(PlantPart)
admin.site.register(Family)
admin.site.register(Microorganism)
