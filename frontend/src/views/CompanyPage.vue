<template>
  <div v-if="company" class="fr-container mb-8 flex flex-col">
    <div class="flex justify-between">
      <SectionTitle :title="company.socialName" icon="ri-home-4-line" />
      <div v-if="!isEditing">
        <DsfrButton @click="isEditing = true" label="Modifier les informations" icon="ri-edit-line" size="sm" />
      </div>
    </div>
    <div v-if="isEditing">
      <CompanyForm
        @responseReady="handleResponse"
        @editCancelled="isEditing = false"
        :initialState="company"
        :url="singleCompanyUrl"
        method="put"
        showCancelButton
      />
    </div>
    <div v-else class="flex flex-col gap-y-10">
      <TabularDataDisplayer title="Informations administratives de l'entreprise" :dataLines="AdminInfoLines" />
      <TabularDataDisplayer title="Activités de l'entreprise" :dataLines="activityLines" />
      <TabularDataDisplayer title="Informations de contact" :dataLines="contactLines" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { useRoute } from "vue-router"
import { headers } from "@/utils/data-fetching"
import { useRootStore } from "@/stores/root"
import useToaster from "@/composables/use-toaster"
import SectionTitle from "@/components/SectionTitle"
import CompanyForm from "@/components/CompanyForm"
import TabularDataDisplayer from "@/components/TabularDataDisplayer"
import { setDocumentTitle } from "@/utils/document"

const route = useRoute()
const rootStore = useRootStore()

// Données pour l'affichage des différentes sections en lecture

const AdminInfoLines = computed(() => {
  const displayableAddress = (company) => {
    /* affichage propre d'une adresse complète */
    const lines = [
      company.address,
      company.additionalDetails,
      `${company.postalCode} ${company.city}`,
      company.cedex,
      company.countryLabel,
    ]
    return lines.filter((line) => line !== "").join("\n")
  }

  return [
    { title: "Dénomination sociale", val: company.value.socialName },
    { title: "Nom commercial", val: company.value.commercialName },
    company.value.siret ? { title: "N° SIRET", val: company.value.siret } : null,
    company.value.vat ? { title: "N° TVA", val: company.value.vat } : null,
    {
      title: "Adresse",
      val: displayableAddress(company.value),
    },
  ].filter((item) => item !== null)
})

const activityLines = computed(() => {
  return [{ title: "Activités enregistrées", val: company.value.activities.map((x) => x.toLowerCase()).join("\n") }]
})

const contactLines = computed(() => {
  return [
    { title: "N° de téléphone de contact", val: company.value.phoneNumber },
    { title: "Adresse e-mail de contact", val: company.value.email },
    { title: "Site web de l'entreprise", val: company.value.website || "-" },
  ]
})

// Edition
const isEditing = ref(false)
const singleCompanyUrl = `/api/v1/companies/${route.params.id}`

// Requête initiale
const {
  data: company,
  response,
  execute,
} = useFetch(
  singleCompanyUrl,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

onMounted(async () => {
  await execute()
  await handleError(response)
  setDocumentTitle([company.value.socialName, "Mon entreprise"])
})

// Gère la réponse du component enfant
const handleResponse = (data) => {
  if (data.value) {
    company.value = data.value
    isEditing.value = false
    rootStore.fetchInitialData() // MAJ du state global car le nom de l'entreprise peut avoir changé
    useToaster().addSuccessMessage("L'entreprise a bien été modifiée")
    window.scrollTo(0, 0)
  }
}
</script>
