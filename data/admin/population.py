from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import Population

from .abstract_admin import ChangeReasonAdminMixin, ChangeReasonFormMixin


class PopulationForm(ChangeReasonFormMixin):
    pass


@admin.register(Population)
class PopulationAdmin(ChangeReasonAdminMixin, SimpleHistoryAdmin):
    form = PopulationForm
    fields = [
        "change_reason",
        "name",
        "category",
        "is_obsolete",
        "is_defined_by_anses",
        "min_age",
        "max_age",
        "creation_date",
        "modification_date",
    ]
    readonly_fields = [
        "name",
        "is_obsolete",
        "creation_date",
        "modification_date",
    ]
    list_display = [
        "name",
        "modification_date",
        "is_defined_by_anses",
    ]
    list_filter = (
        "is_obsolete",
        "is_defined_by_anses",
    )
    show_facets = admin.ShowFacets.NEVER
