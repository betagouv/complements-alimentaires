<template>
  <div class="p-6">
    <SectionHeader id="declarant-e" text="Déclarant·e" icon="ri-user-fill" />
    <DeclarantIdentity class="mb-8" :user="declarant" />
    <SectionHeader id="entreprise" text="Identité de l’entreprise" icon="ri-building-4-fill" />
    <CompanyIdentity :company="company" :mandatedCompany="mandatedCompany" />

    <DsfrButton class="mt-4" label="Voir tous les produits de cette entreprise" @click="openCompanyPage" />
  </div>
</template>

<script setup>
import SectionHeader from "@/components/NewBepiasViews/SectionHeader"
import DeclarantIdentity from "@/components/DeclarantIdentity"
import CompanyIdentity from "@/components/CompanyIdentity"
import { useRouter } from "vue-router"

const props = defineProps({ declarant: Object, company: Object, mandatedCompany: Object })
const router = useRouter()
const openCompanyPage = () => router.push({ name: "CompanyDetails", params: { companyId: props.company.id } })
</script>
