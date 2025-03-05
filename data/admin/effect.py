from django import forms
from django.contrib import admin

from simple_history.admin import SimpleHistoryAdmin

from data.models import Effect

from .abstract_admin import ChangeReasonAdminMixin


class EffectForm(forms.ModelForm):
    class Meta:
        widgets = {
            "ca_name": forms.Textarea(attrs={"cols": 60, "rows": 1}),
            "change_reason": forms.TextInput(attrs={"size": "70"}),
        }

    # saved in ChangeReasonAdminMixin.save()
    change_reason = forms.CharField(
        label="Raison de modification",
        help_text="100 caractères max",
        max_length=100,
    )


@admin.register(Effect)
class EffectAdmin(ChangeReasonAdminMixin, SimpleHistoryAdmin):
    form = EffectForm
    fields = [
        "change_reason",
        "name",
        "ca_name",
        "siccrf_name_en",
        "is_obsolete",
        "ca_is_obsolete",
        "creation_date",
        "modification_date",
    ]
    readonly_fields = [
        "name",
        "siccrf_name_en",
        "is_obsolete",
        "creation_date",
        "modification_date",
    ]
    list_display = [
        "name",
        "modification_date",
    ]
    list_filter = ("is_obsolete",)
    show_facets = admin.ShowFacets.NEVER
