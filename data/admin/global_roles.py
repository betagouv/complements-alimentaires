from django.contrib import admin

from data.models import InstructionRole


@admin.register(InstructionRole)
class InstructionRoleAdmin(admin.ModelAdmin):
    pass
