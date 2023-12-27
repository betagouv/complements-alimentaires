from django.contrib import admin

from .user import UserAdmin  # noqa
from .blogpost import BlogPostAdmin  # noqa
from .webinar import WebinarAdmin  # noqa
from .substance import SubstanceAdmin  # noqa

from data.models import Ingredient, Plant, PlantPart, PlantFamily, Microorganism  # noqa

admin.site.register(Ingredient)
admin.site.register(Plant)
admin.site.register(PlantPart)
admin.site.register(PlantFamily)
admin.site.register(Microorganism)
