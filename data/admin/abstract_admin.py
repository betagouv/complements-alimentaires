class ChangeReasonAdminMixin:
    def save_model(self, request, obj, form, change):
        if change:
            obj._change_reason = (
                form.cleaned_data["change_reason"]
                if "change_reason" in form.cleaned_data.keys()
                else "Modification via l'admin"
            )

        super().save_model(request, obj, form, change)
