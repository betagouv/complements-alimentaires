from django.contrib import admin

from ..models.company import EtablissementToCompanyRelation  # , Company


@admin.register(EtablissementToCompanyRelation)
class EtablissementToCompanyRelationAdmin(admin.ModelAdmin):
    list_display = ("__str__", "old_vat", "old_siret")
    readonly_fields = (
        "siccrf_id",
        "siccrf_registration_date",
    )

    search_fields = ("old_vat", "old_siret", "company__social_name", "company__id")

    def save_related(self, request, form, formsets, change):
        for formset in formsets:
            # Found this simple way to check dynamic class instance.
            if formset.model == EtablissementToCompanyRelation:
                # instances = formset.save(commit=False)
                # hostel = form.instance

                for added_historic_siret in formset.new_objects:
                    pass
                    # ajoute le siccrf_id à la relation
                    # une relation avec ce siccrf_id existe déjà
                    # historic_etablissement = IcaEtablissement(etab_siret=added_historic_siret)

                    # relation = EtablissementToCompanyRelation.objects.get(siccrf_id=historic_etablissement.etab_ident)
                    # old_company_id = relation.company_id
                    # declarations_to_change_company = Declaration.objects.filter(company_id=old_company_id)
                    # for declaration in declarations_to_change_company:
                    #     declaration.company = new_company
                    #     declaration.save()
                    # # importe les déclarations de l'établissement
                    # relation.company_id = new_company_id
                    # relation.save()
                    # soft delete l'ancien établissement

        super().save_related(request, form, formsets, change)
