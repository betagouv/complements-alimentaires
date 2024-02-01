from django.contrib import admin

from .user import UserAdmin  # noqa
from .blogpost import BlogPostAdmin  # noqa
from .webinar import WebinarAdmin  # noqa
from .substance import SubstanceAdmin  # noqa
from .plant import PlantAdmin  # noqa
from .population import Population  # noqa

from data.models import Ingredient, PlantPart, PlantFamily, Microorganism


def get_admin_header():
    return "Compl'Alim"


admin.site.register(Ingredient)
admin.site.register(PlantPart)
admin.site.register(PlantFamily)
admin.site.register(Microorganism)


admin.site.site_header = get_admin_header()
admin.site.site_title = get_admin_header()
