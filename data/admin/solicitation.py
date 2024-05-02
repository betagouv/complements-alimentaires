from django.contrib import admin

from data.models import Solicitation


@admin.register(Solicitation)
class SolicitationAdmin(admin.ModelAdmin):
    list_display = ("id", "creation_date", "kind", "sender", "display_recipients", "process_state")

    def process_state(self, obj):
        return "✅ Traitée" if obj.is_processed else "🕣 Non traitée"

    def display_recipients(self, obj):
        recipient_count = obj.recipients.count()
        if recipient_count == 1:
            return obj.recipient.get().name
        else:
            return f"{recipient_count} destinataires"

    process_state.short_description = "État du traitement"
    display_recipients.short_description = "Destinataire(s)"
