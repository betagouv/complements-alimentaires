from django.contrib import admin

from data.models import ControlRole, InstructionRole, VisaRole


@admin.register(InstructionRole)
class InstructionRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(VisaRole)
class VisaRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(ControlRole)
class ControlRoleAdmin(admin.ModelAdmin):
    pass
