from django.contrib import admin

from ..models.roles import Declarant, Supervisor


@admin.register(Declarant)
class DeclarantAdmin(admin.ModelAdmin):
    pass


@admin.register(Supervisor)
class SupervisorAdmin(admin.ModelAdmin):
    pass
