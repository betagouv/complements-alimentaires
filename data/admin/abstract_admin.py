from simple_history.utils import update_change_reason


class ChangeReasonAdminMixin:
    def save_model(self, request, obj, form, change):
        if change:
            update_change_reason(
                obj,
                form.cleaned_data["change_reason"]
                if "change_reason" in form.cleaned_data.keys()
                else "Modification de l'ingrédient",
            )

        super().save_model(request, obj, form, change)
