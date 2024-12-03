from rest_framework import serializers


class PrivateCommentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context and self.context["request"] and self.context["request"].user
        if not user:
            self.remove_fields(repr)
            return repr
        try:
            has_visa_role = user.visarole
        except Exception as _:
            has_visa_role = False
        try:
            has_instruction_role = user.instructionrole
        except Exception as _:
            has_instruction_role = False
        can_see_private_comments = has_visa_role or has_instruction_role
        if not can_see_private_comments:
            self.remove_fields(repr)
        return repr

    def remove_fields(self, representation):
        fields = getattr(self, "private_fields", ("private_comments",))
        for field in fields:
            representation.pop(field, None)


class HistoricalModelSerializer(serializers.ModelSerializer):
    """
    Si le serializer contient un champ "history", ce champ sera conditionné à
    `context.history`. Ceci permet de ne pas requeter la table de simple-history
    à moins que ça soit explicitement requis par la view.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.context.get("history", None):
            self.fields.pop("history", None)
