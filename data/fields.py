from django import forms
from django.contrib.postgres.fields import ArrayField


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
