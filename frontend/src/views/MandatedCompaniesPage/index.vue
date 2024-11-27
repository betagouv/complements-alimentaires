<template>
  <div class="fr-container mb-8">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Entreprises mandatées' }]"
    />
    <h1 class="fr-h3">Entreprises mandatées</h1>
    <div v-if="company">
      <p>
        Une entreprise mandatée peut effectuer des déclarations au nom de {{ company.socialName }}.

        <span v-if="hasMandates">
          Il y a {{ company.mandatedCompanies.length }}
          <span v-if="company.mandatedCompanies.length === 1">mandat</span>
          <span v-else>mandats</span>
          en cours pour {{ company.socialName }}.
        </span>
        <span v-else>Il n'y a pas de mandats en cours pour {{ company.socialName }}.</span>
      </p>
      <MandatedCompaniesList
        v-if="hasMandates"
        :mandatedCompanies="company.mandatedCompanies"
        @remove="removeMandate"
      />
      <div>
        <NewMandateModal @confirm="addMandate" />
      </div>
    </div>
    <div v-else class="flex justify-center items-center min-h-60">
      <ProgressSpinner />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import useToaster from "@/composables/use-toaster"
import { useFetch } from "@vueuse/core"
import { useRoute } from "vue-router"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"
import { onMounted } from "vue"
import ProgressSpinner from "@/components/ProgressSpinner"
import NewMandateModal from "./NewMandateModal"
import MandatedCompaniesList from "./MandatedCompaniesList"

const route = useRoute()
const {
  data: company,
  execute,
  response,
} = useFetch(`/api/v1/companies/${route.params.id}`, { headers: headers() }, { immediate: false }).json()

onMounted(async () => {
  await execute()
  await handleError(response)
})

const addMandate = (siret, vat) => {
  const payload = { siret, vat }
  const url = `/api/v1/companies/${route.params.id}/add-mandated-company/`
  const successMessage = "L'entreprise mandatée a bien été ajoutée"
  editMandate(payload, url, successMessage)
}

const removeMandate = (id) => {
  const payload = { id }
  const url = `/api/v1/companies/${route.params.id}/remove-mandated-company/`
  const successMessage = `L'entreprise mandatée a bien été supprimée. Elle ne pourra plus déclarer au nom de ${company.value.socialName}.`
  editMandate(payload, url, successMessage)
}

const editMandate = async (payload, url, successMessage) => {
  const { response: mandateResponse, data } = await useFetch(url, { headers: headers() }).post(payload).json()
  if (!mandateResponse.value.ok) {
    useToaster().addErrorMessage("Une erreur s'est produite, merci de ressayer plus tard")
    return
  }
  company.value = data.value
  useToaster().addSuccessMessage(successMessage)
}

const hasMandates = computed(() => company.value?.mandatedCompanies?.length > 0)
</script>
