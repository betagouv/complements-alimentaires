from rest_framework import serializers


class GoodReprChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        return self.choices[obj]

    def to_internal_value(self, data):
        return getattr(self.choices, data)
