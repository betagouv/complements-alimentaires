from django.contrib import admin
from ..models.roles import Declarant, CompanySupervisor


@admin.register(Declarant)
class DeclarantAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanySupervisor)
class CompanySupervisorAdmin(admin.ModelAdmin):
    pass
