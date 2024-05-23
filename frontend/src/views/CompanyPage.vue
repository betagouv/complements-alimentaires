<template>
  <div v-if="company" class="fr-container my-8 flex flex-col">
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
    <div v-else>
      <p class="font-bold">Informations administratives de l'entreprise</p>
      <div class="grid grid-col-3 border-t border-gray-100">
        <div class="divide-y divide-gray-100">
          <div v-for="line in companyLines" :key="line.title" class="grid grid-cols-3 py-5 whitespace-pre-line">
            <dt class="font-medium">{{ line.title }}</dt>
            <dd class="text-gray-700">{{ line.val }}</dd>
          </div>
        </div>
      </div>
      <p class="font-bold mt-4">Activités de l'entreprise</p>
      <div class="grid grid-col-3 border-t border-gray-100">
        <div class="divide-y divide-gray-100">
          <div class="grid grid-cols-3 py-5 whitespace-pre-line">
            <dt class="font-medium">Activités enregistrées</dt>
            <dd class="text-gray-700">
              <ul class="m-0">
                <li v-for="activity in company.activities" :key="activity">
                  {{ activity.toLowerCase() }}
                </li>
              </ul>
            </dd>
          </div>
        </div>
      </div>
      <p class="font-bold mt-4">Informations de contact</p>
      <div class="grid grid-col-3 border-t border-gray-100">
        <div class="divide-y divide-gray-100">
          <div v-for="line in contactLines" :key="line.title" class="grid grid-cols-3 py-5 whitespace-pre-line">
            <dt class="font-medium">{{ line.title }}</dt>
            <dd class="text-gray-700">{{ line.val }}</dd>
          </div>
        </div>
      </div>
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

const route = useRoute()
const rootStore = useRootStore()

// Lecture

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

const companyLines = computed(() => {
  return [
    company.value.siret ? { title: "N° SIRET", val: company.value.siret } : null,
    company.value.vat ? { title: "N° VAT", val: company.value.vat } : null,
    { title: "Dénomination sociale", val: company.value.socialName },
    { title: "Nom commercial", val: company.value.commercialName },
    {
      title: "Adresse",
      val: displayableAddress(company.value),
    },
  ].filter((item) => item !== null)
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
})

// Gère la réponse du component enfant
const handleResponse = (data) => {
  if (data.value) {
    company.value = data.value
    isEditing.value = false
    rootStore.fetchInitialData()
    useToaster().addSuccessMessage("L'entreprise a bien été modifiée")
  }
}
</script>
