<template>
  <div v-if="company">
    <div v-if="mandatedCompany" class="border p-2 mb-4">
      <p class="mb-0">
        <v-icon name="ri-information-fill" />
        L'entreprise {{ mandatedCompany.socialName }}
        <span v-if="mandatedCompany.siret">(SIRET : {{ mandatedCompany.siret }})</span>
        <span v-else-if="mandatedCompany.vat">(TVA : {{ mandatedCompany.vat }})</span>
        a été mandatée pour la déclaration de ce complément.
      </p>
    </div>
    <p class="font-bold">{{ company.socialName }}</p>
    <p v-if="company.siret">
      Numéro SIRET : {{ company.siret }}
      <ExternalLink
        :href="`https://annuaire-entreprises.data.gouv.fr/etablissement/${company.siret}`"
        text="(voir dans l'annuaire des entreprises)"
        style="color: var(--text-default-grey)"
      />
    </p>

    <p v-if="company.vat">Numéro de TVA : {{ company.vat }}</p>
    <p v-if="company.phoneNumber">
      Numéro téléphone :
      <a :href="`tel:${company.phoneNumber}`">{{ company.phoneNumber }}</a>
    </p>
    <p v-if="company.address">
      <span>
        Adresse :
        <AddressLine class="inline" :payload="company" />
      </span>
    </p>
  </div>
  <p v-else>Cette déclaration n'a pas d'entreprise associée. La compagnie a probablement été supprimé depuis.</p>
</template>

<script setup>
import AddressLine from "@/components/AddressLine"
import ExternalLink from "@/components/ExternalLink"
defineProps({ company: Object, mandatedCompany: Object })
</script>

<style scoped>
@reference "../styles/index.css";
p {
  @apply mb-2!;
}
</style>
