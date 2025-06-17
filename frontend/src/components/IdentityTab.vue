<template>
  <div>
    <SectionTitle title="Entreprise" icon="ri-home-2-fill" />
    <CompanyIdentity :company="company" />

    <SectionTitle class="mt-8!" title="Déclarant ou déclarante" icon="ri-user-fill" />
    <DeclarantIdentity :user="user" />
  </div>
</template>

<script setup>
import SectionTitle from "@/components/SectionTitle"
import DeclarantIdentity from "@/components/DeclarantIdentity"
import CompanyIdentity from "@/components/CompanyIdentity"
defineProps({ user: Object, company: Object })
</script>

<style scoped>
@reference "../styles/index.css";

p {
  @apply mb-2!;
}
</style>
