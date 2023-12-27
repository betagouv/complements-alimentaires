from django import forms
from django.contrib import admin
from django.utils import timezone
from data.models import Webinar


class WebinarForm(forms.ModelForm):
    class Meta:
        widgets = {
            "title": forms.Textarea(attrs={"cols": 35, "rows": 1}),
            "tagline": forms.Textarea(attrs={"cols": 65, "rows": 3}),
            "link": forms.Textarea(attrs={"cols": 70, "rows": 1}),
        }


class UpcomingEventsFilter(admin.SimpleListFilter):
    title = "date"

    parameter_name = "upcoming_status"

    def lookups(self, request, model_admin):
        return (
            ("future", "À venir"),
            ("past", "Passé"),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        elif self.value() in ("future"):
            return queryset.filter(end_date__gt=timezone.now())
        elif self.value() in ("past"):
            return queryset.filter(end_date__lte=timezone.now())


@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    form = WebinarForm
    fields = (
        "title",
        "tagline",
        "start_date",
        "end_date",
        "link",
    )
    list_display = (
        "title",
        "start_date",
    )
    list_filter = (UpcomingEventsFilter,)
