from django.contrib import admin

from data.models import CollaborationInvitation, CoSupervisionClaim, SupervisionClaim


class BaseSolicitationAdmin:
    list_display = ("id", "creation_date", "sender", "display_recipients", "process_state")

    def process_state(self, obj):
        return "✅ Traitée" if obj.processed_at else "🕣 Non traitée"

    process_state.short_description = "État du traitement"

    readonly_fields = ["processed_at", "processor", "processed_action"]


class WithDisplayRecipients:
    def display_recipients(self, obj):
        recipient_count = obj.recipients.count()
        if recipient_count == 1:
            return obj.recipient.get().name
        else:
            return f"{recipient_count} destinataires"

    display_recipients.short_description = "Destinataire(s)"


@admin.register(SupervisionClaim)
class SupervisionClaimAdmin(BaseSolicitationAdmin, WithDisplayRecipients, admin.ModelAdmin):
    pass


@admin.register(CoSupervisionClaim)
class CoSupervisionClaimAdmin(BaseSolicitationAdmin, WithDisplayRecipients, admin.ModelAdmin):
    pass


@admin.register(CollaborationInvitation)
class CollaborationInvitation(BaseSolicitationAdmin, admin.ModelAdmin):
    def display_recipients(self, obj):
        return obj.recipient_email

    display_recipients.short_description = "Destinataire"
