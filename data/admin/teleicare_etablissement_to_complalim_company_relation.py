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
            declarations_to_move = Declaration.objects.filter(company_id=old_company_id).exclude(siccrf_id=None)
            for declaration in declarations_to_move:
                declaration.company_id = new_company_id
                declaration.save()
                update_change_reason(declaration, change_reason)

            messages.add_message(
                request,
                messages.INFO,
                f"{declarations_to_move.count()} déclarations transférées de l'entreprise {old_company_id} à l'entreprise {new_company_id}",
            )
            if Declaration.objects.filter(company_id=old_company_id).count() == 0:
                messages.add_message(
                    request, messages.INFO, f"Vous devez supprimer manuellement l'entreprise {old_company_id}"
                )
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    f"L'entreprise {old_company_id} issue de TéléIcare, est rattachée à des déclarations Compl'Alim",
                )

            # Suppression manuelle de la Company
            # old_company = Company.objects.get(id=old_company_id)
            # old_company.delete()
        super().save_model(request, obj, form, change)
