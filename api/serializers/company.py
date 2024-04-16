from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from data.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "social_name",
            "commercial_name",
            "siret",
            "vat",
            "address",
            "additional_details",
            "postal_code",
            "city",
            "cedex",
            "country",
            "activities",
            "phone_number",
            "email",
            "website",
        )

    id = serializers.IntegerField(read_only=True)
    phone_number = PhoneNumberField()

    def to_internal_value(self, data):
        # permet de définir dynamiquement la bonne région pour le numéro de téléphone entré
        self.fields["phone_number"] = PhoneNumberField(region=data["country"])
        return super().to_internal_value(data)
