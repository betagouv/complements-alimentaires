from rest_framework import serializers


class PrivateCommentSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        user = self.context and self.context["request"] and self.context["request"].user
        if not user:
            repr.pop("private_comments")
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
            repr.pop("private_comments", None)
        return repr
