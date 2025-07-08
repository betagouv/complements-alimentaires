from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from data.models import Company, DeclarantRole, SupervisorRole


class MinimalCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "social_name",
            "siret",
            "vat",
        )


class SimpleCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "social_name",
            "postal_code",
            "city",
            "cedex",
            "country",
        )


class ControllerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "id",
            "social_name",
            "address",
            "additional_details",
            "postal_code",
            "activities",
            "country",
        )


class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    phone_number = PhoneNumberField()
    country_label = serializers.CharField(read_only=True, source="get_country_display")
    mandated_companies = MinimalCompanySerializer(read_only=True, many=True)
    represented_companies = MinimalCompanySerializer(read_only=True, many=True)

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
            "country_label",
            "activities",
            "phone_number",
            "email",
            "website",
            "mandated_companies",
            "represented_companies",
        )
        read_only_fields = (
            "mandated_companies",
            "represented_companies",
        )

    def to_internal_value(self, data):
        # permet de définir dynamiquement la bonne région pour le numéro de téléphone entré
        self.fields["phone_number"] = PhoneNumberField(region=data["country"])
        return super().to_internal_value(data)


class BaseRoleSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        fields = ("id", "name")

    def get_name(self, obj):
        return obj.__class__.__name__


class SupervisorRoleSerializer(BaseRoleSerializer):
    class Meta:
        model = SupervisorRole
        fields = BaseRoleSerializer.Meta.fields


class DeclarantRoleSerializer(BaseRoleSerializer):
    class Meta:
        model = DeclarantRole
        fields = BaseRoleSerializer.Meta.fields
