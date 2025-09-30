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
    list_display = ("user", "persistant")

    def persistant(self, obj):
        return "🔒 Reste même si absent sur Grist" if obj.always_persist else " "
