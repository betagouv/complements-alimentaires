from django import forms
from django.contrib.postgres.fields import ArrayField

from prose.fields import RichTextField
from prose.widgets import RichTextEditor


class MultipleChoiceField(ArrayField):
    """
    Un ArrayField permettant de sélectionner plusieurs éléments, utilisant un widget de type Checkbox côté template/admin.
    Explications ici : https://rogulski.it/django-multiselect-choice-admin/
    """

    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
            "widget": forms.CheckboxSelectMultiple,
            **kwargs,
        }
        return super(ArrayField, self).formfield(**defaults)


# L'editeur de Prose a seulement h1 comme entête. Ces éditeurs enrichis ajoutent les
# autres niveaux d'entête.
class EnrichedRichTextEditor(RichTextEditor):
    class Media:
        js = ("extend-buttons.js",)


class EnrichedRichTextField(RichTextField):
    def formfield(self, **kwargs):
        kwargs["widget"] = EnrichedRichTextEditor

        # On a besoin d'appeller directement la superclass de RichTextField car sinon notre
        # kwargs["widget"] est ecrassé par la superclass
        parent_return_value = super(RichTextField, self).formfield(**kwargs)
        return parent_return_value
