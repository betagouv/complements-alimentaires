<template>
  <div>
    <div class="bg-grey-975! p-6">
      <SectionHeader id="declarant-e" text="Déclarant·e" icon="ri-user-fill" />
      <DeclarantIdentity class="mb-8" :user="declarant" />
      <SectionHeader id="produit" text="Informations sur le produit" icon="ri-file-info-fill" />
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
      <SectionHeader id="entreprise" text="Identité de l’entreprise" icon="ri-building-4-fill" />
      <CompanyIdentity :company="company" />
    </div>
  </div>
</template>

<script setup>
import SectionHeader from "../SectionHeader"
import DeclarantIdentity from "@/components/DeclarantIdentity"
import CompanyIdentity from "@/components/CompanyIdentity"

defineProps({ declarant: Object, company: Object })
</script>
