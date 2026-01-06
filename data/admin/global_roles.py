import logging

from django.contrib import admin

from data.models import ControlRole, InstructionRole, VisaRole

logger = logging.getLogger(__name__)


@admin.register(InstructionRole)
class InstructionRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(VisaRole)
class VisaRoleAdmin(admin.ModelAdmin):
    pass


@admin.register(ControlRole)
class ControlRoleAdmin(admin.ModelAdmin):
    list_filter = ["always_persist"]
    list_display = ("user", "persistant", "domaine_email_ok")
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    def persistant(self, obj):
        return "🔒 Reste même si absent sur Grist" if obj.always_persist else " "

    def domaine_email_ok(self, obj):
        user_email = obj.user.email
        government_email = user_email[-8:] in ["@gouv.fr", ".gouv.fr", "@anses.fr"] or user_email[-9:] == "@anses.fr"

        return "" if government_email else f"⚠️ Adresse en « {user_email.split('@')[-1]} »"
