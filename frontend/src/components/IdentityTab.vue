<template>
  <div>
    <SectionTitle title="Entreprise" icon="ri-home-2-fill" />
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
        <AddressLine class="inline" :payload="company" />
      </span>
    </p>
    <SectionTitle class="mt-8!" title="Déclarant ou déclarante" icon="ri-user-fill" />
    <div v-if="user">
      <p>{{ user.firstName }} {{ user.lastName }}</p>
      <p>
        Adresse email :
        <a :href="`mailto:${user.email}`" target="_blank">{{ user.email }}</a>
      </p>
    </div>
    <p v-else>
      Cette déclaration n'a pas de déclarant ou déclarante assigné. Le compte a probablement été supprimé depuis.
    </p>
  </div>
</template>

<script setup>
import SectionTitle from "@/components/SectionTitle"
import AddressLine from "@/components/AddressLine"
defineProps({ user: Object, company: Object })
</script>

<style scoped>
@reference "../../styles/index.css";

p {
  @apply mb-2!;
}
</style>
