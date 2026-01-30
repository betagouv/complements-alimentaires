from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from api.utils.simplified_status import SimplifiedStatusHelper
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
            "address",
            "additional_details",
            "postal_code",
            "city",
            "cedex",
            "country",
        )


class ControllerCompanyListSerializer(serializers.ModelSerializer):
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
            "market_ready_count_cache",
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


class ControllerCompanySerializer(serializers.ModelSerializer):
    total_declarations = serializers.SerializerMethodField()
    market_ready_declarations = serializers.SerializerMethodField()
    refused_declarations = serializers.SerializerMethodField()
    ongoing_declarations = serializers.SerializerMethodField()
    withdrawn_declarations = serializers.SerializerMethodField()
    interrupted_declarations = serializers.SerializerMethodField()

    class Meta:
        model = Company

        fields = (
            "id",
            "social_name",
            "commercial_name",
            "total_declarations",
            "market_ready_declarations",
            "refused_declarations",
            "ongoing_declarations",
            "withdrawn_declarations",
            "interrupted_declarations",
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
        read_only_fields = fields

    def get_total_declarations(self, obj):
        return obj.declarations.count()

    def get_market_ready_declarations(self, obj):
        return self._count_for_simplified_status(obj, SimplifiedStatusHelper.MARKET_READY)

    def get_refused_declarations(self, obj):
        return self._count_for_simplified_status(obj, SimplifiedStatusHelper.REFUSED)

    def get_ongoing_declarations(self, obj):
        return self._count_for_simplified_status(obj, SimplifiedStatusHelper.ONGOING)

    def get_withdrawn_declarations(self, obj):
        return self._count_for_simplified_status(obj, SimplifiedStatusHelper.WITHDRAWN)

    def get_interrupted_declarations(self, obj):
        return self._count_for_simplified_status(obj, SimplifiedStatusHelper.INTERRUPTED)

    def _count_for_simplified_status(self, obj, status):
        return obj.declarations.filter(SimplifiedStatusHelper.get_filter_conditions([status])).count()


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


class ControlCompanyExcelSerializer(serializers.ModelSerializer):
    # Champ spécial utilisé par drf-excel documenté ici : https://github.com/django-commons/drf-excel
    row_color = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = (
            "id",
            "social_name",
            "siret",
            "vat",
            "department",
            "row_color",  # Champ utilisé en interne par drf-excel
        )
        read_only_fields = fields

    def get_row_color(self, instance):
        """
        Permet d'alterner les couleurs des files dans le ficher Excel
        """
        return ["FFFFFFFF", "FFECECFE"][(*self.instance,).index(instance) % 2]
