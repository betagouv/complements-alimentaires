<template>
  <div class="p-6">
    <SectionHeader id="declarant-e" text="Déclarant·e" icon="ri-user-fill" />
    <DeclarantIdentity class="mb-8" :user="declarant" />
    <SectionHeader id="entreprise" text="Identité de l’entreprise" icon="ri-building-4-fill" />
    <CompanyIdentity :company="company" :mandatedCompany="mandatedCompany" />

    <router-link :to="{ name: 'CompanyDetails', params: { companyId: company.id } }" class="mt-4 fr-btn">
      Voir tous les produits de cette entreprise
    </router-link>
  </div>
</template>

<script setup>
import SectionHeader from "@/components/NewBepiasViews/SectionHeader"
import DeclarantIdentity from "@/components/DeclarantIdentity"
import CompanyIdentity from "@/components/CompanyIdentity"

defineProps({ declarant: Object, company: Object, mandatedCompany: Object })
</script>
