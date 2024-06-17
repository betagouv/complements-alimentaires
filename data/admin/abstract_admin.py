from simple_history.admin import SimpleHistoryAdmin


class ElementAdminWithChangeReason(SimpleHistoryAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            # TODO: la change reason devrait pouvoir être renseignée dans le form
            obj._change_reason = "Modification de l'ingrédient"
        super().save_model(request, obj, form, change)
