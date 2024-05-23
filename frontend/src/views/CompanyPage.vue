<template>
  <div v-if="company" class="fr-container my-8 flex flex-col">
    <div class="flex justify-between">
      <SectionTitle :title="company.socialName" icon="ri-home-4-line" />
      <div v-if="!isEditing">
        <DsfrButton @click="isEditing = true" label="Modifier les informations" icon="ri-edit-line" size="sm" />
      </div>
    </div>
    <p>Consultez et mettez à jour les données de votre entreprise</p>
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
      <p>formulaire readonly</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
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
