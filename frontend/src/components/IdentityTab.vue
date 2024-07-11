<template>
  <div>
    <SectionTitle title="Déclarant ou déclarante" icon="ri-user-fill" />
    <p>{{ user.firstName }} {{ user.lastName }}</p>
    <p>
      Adresse email :
      <a :href="`mailto:${user.email}`" target="_blank">{{ user.email }}</a>
    </p>

    <SectionTitle class="!mt-8" title="Entreprise" icon="ri-home-2-fill" />
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
      <span>
        Adresse :
        <address class="inline">
          {{ company.address }}
          {{ company.additional_details }}
          {{ company.postal_code }}
          {{ company.city }}
          {{ company.country }}
          <span v-if="company.cedex">- CEDEX : {{ company.cedex }}</span>
        </address>
      </span>
    </p>
  </div>
</template>

<script setup>
import SectionTitle from "@/components/SectionTitle"
defineProps({ user: Object, company: Object })
</script>

<style scoped>
p {
  @apply !mb-2;
}
</style>
