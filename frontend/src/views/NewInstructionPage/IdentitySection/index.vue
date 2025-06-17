<template>
  <div>
    <div class="bg-grey-975! p-6">
      <SectionHeader id="declarant-e" text="Déclarant·e" icon="ri-user-fill" />
      <DeclarantIdentity class="mb-8" :user="declarant" />
      <SectionHeader id="produit" text="Informations sur le produit" icon="ri-file-info-fill" />
      <ProductInfoSegment class="mb-8" :payload="declaration" />
      <SectionHeader id="entreprise" text="Identité de l’entreprise" icon="ri-building-4-fill" />
      <CompanyIdentity :company="company" />
    </div>
  </div>
</template>

<script setup>
import SectionHeader from "../SectionHeader"
import DeclarantIdentity from "@/components/DeclarantIdentity"
import CompanyIdentity from "@/components/CompanyIdentity"
import ProductInfoSegment from "@/components/ProductInfoSegment"

defineProps({ declarant: Object, company: Object, declaration: Object })
</script>
