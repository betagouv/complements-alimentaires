<template>
  <div v-if="company">
    <p class="font-bold">{{ company.socialName }}</p>
    <p v-if="company.siret">
      Numéro SIRET : {{ company.siret }}
      <a
        class="ml-1"
        :href="`https://annuaire-entreprises.data.gouv.fr/etablissement/${company.siret}`"
        target="_blank"
      >
        (voir dans l'annuaire des entreprises)
      </a>
    </p>

    <p v-if="company.vat">Numéro de TVA : {{ company.vat }}</p>
    <p v-if="company.phoneNumber">
      Numéro téléphone :
      <a :href="`tel:${company.phoneNumber}`" target="_blank">{{ company.phoneNumber }}</a>
    </p>
    <p v-if="company.address">
      {{ company.address }}
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
defineProps({ company: Object })
</script>

<style scoped>
@reference "../styles/index.css";
p {
  @apply mb-2!;
}
</style>
