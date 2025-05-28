from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join, mark_safe

from ..models.company import Company, DeclarantRole, EtablissementToCompanyRelation, SupervisorRole
from .abstract_admin import ChangeReasonAdminMixin, ChangeReasonFormMixin


class SupervisionInline(admin.TabularInline):
    model = Company.supervisors.through
    extra = 0


class DeclarantInline(admin.TabularInline):
    model = Company.declarants.through
    extra = 0


class EtablissementToCompanyRelationInline(admin.TabularInline):
    model = EtablissementToCompanyRelation
    readonly_fields = ("siccrf_id", "siccrf_registration_date")
    extra = 0


class CompanyForm(ChangeReasonFormMixin):
    pass


@admin.register(Company)
class CompanyAdmin(ChangeReasonAdminMixin, admin.ModelAdmin):
    form = CompanyForm
    filter_horizontal = ("mandated_companies",)
    readonly_fields = ("display_represented_companies",)

    search_fields = (
        "social_name",
        "commercial_name",
        "vat",
        "siret",
    )

    fieldsets = (
        (
            None,
            {"fields": ["change_reason"]},
        ),
        (
            "",
            {
                "fields": (
                    "social_name",
                    "commercial_name",
                    "siret",
                    "vat",
                    "activities",
                )
            },
        ),
        (
            "Contact",
            {
                "fields": (
                    "phone_number",
                    "email",
                    "website",
                )
            },
        ),
        (
            "Adresse",
            {
                "fields": (
                    "address",
                    "additional_details",
                    "postal_code",
                    "city",
                    "cedex",
                    "country",
                )
            },
        ),
        (
            "Mandats",
            {
                "fields": (
                    "mandated_companies",
                    "display_represented_companies",
                )
            },
        ),
    )

    inlines = (
        SupervisionInline,
        DeclarantInline,
        EtablissementToCompanyRelationInline,
    )

    def display_represented_companies(self, obj):
        """
        Affiche la relation inversé de `mandated_companies`, çad `represented_companies`
        en tant que liste formatée
        """
        represented = obj.represented_companies.all()
        if represented.exists():
            list_items = format_html_join(
                mark_safe(""),
                '<li><a href="{}">{}</a></li>',
                (
                    (
                        reverse("admin:data_company_change", args=(company.id,)),
                        f"{company.social_name or company.commercial_name} ({company.siret or company.vat})",
                    )
                    for company in represented
                ),
            )
            return format_html('<ul style="margin-left:0;">{}</ul>', list_items)
        return "Cette entreprise peut seulement déclarer pour elle-même."

    display_represented_companies.short_description = "Entreprises representées"


@admin.register(SupervisorRole)
class SupervisorRoleAdmin(admin.ModelAdmin):
    search_fields = (
        "user__first_name",
        "user__last_name",
        "company__social_name",
        "company__commercial_name",
    )


@admin.register(DeclarantRole)
class DeclarantRoleAdmin(admin.ModelAdmin):
    search_fields = (
        "user__first_name",
        "user__last_name",
        "company__social_name",
        "company__commercial_name",
    )
