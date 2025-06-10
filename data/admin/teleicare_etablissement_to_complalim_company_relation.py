from django.contrib import admin, messages

from simple_history.utils import update_change_reason

from ..models.company import EtablissementToCompanyRelation
from ..models.declaration import Declaration


@admin.register(EtablissementToCompanyRelation)
class EtablissementToCompanyRelationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "old_vat", "old_siret")
    readonly_fields = (
        "siccrf_id",
        "etablissement_teleicare",
        "siccrf_registration_date",
    )

    search_fields = ("old_vat", "old_siret", "company__social_name", "company__id")

    def save_model(self, request, obj, form, change):
        """
        si la company a changé :
        * transfère les déclarations de l'ancienne company à la nouvelle
        * et supprime l'ancienne company
        """
        if change and form["company"]._has_changed():
            old_company_id = self.model.objects.get(id=obj.id).company_id
            new_company_id = int(form["company"].value())
            change_reason = (
                f"Transfert des déclarations de l'entreprise {old_company_id} à l'entreprise {new_company_id}"
            )
            messages.add_message(request, messages.INFO, change_reason)

            for declaration in Declaration.objects.filter(company_id=old_company_id):
                declaration.company_id = new_company_id
                declaration.save()
                update_change_reason(declaration, change_reason)

            messages.add_message(
                request, messages.INFO, f"Vous devez supprimer manuellement l'entreprise {old_company_id}"
            )

            # Suppression manuelle de la Company
            # old_company = Company.objects.get(id=old_company_id)
            # old_company.delete()
        super().save_model(request, obj, form, change)
