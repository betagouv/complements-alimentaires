<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: '/tableau-de-bord', text: 'Tableau de bord' }, { text: 'Toutes les déclarations' }]"
    />
    <div class="border px-4 mb-2 sm:flex gap-8 items-baseline filters">
      <DsfrInputGroup>
        <DsfrSelect
          :modelValue="filteredStatus"
          label="Filtrer par statut"
          :options="statusFilterOptions"
          @update:modelValue="updateStatusFilter"
        />
      </DsfrInputGroup>
      <DsfrFieldset legend="Nom d'entreprise" class="!mb-0">
        <div class="flex gap-4">
          <DsfrInputGroup>
            <DsfrInput class="max-w-28" label="De :" label-visible @update:modelValue="updateStatusFilter" />
          </DsfrInputGroup>
          <DsfrInputGroup>
            <DsfrInput class="max-w-28" label="À :" label-visible @update:modelValue="updateStatusFilter" />
          </DsfrInputGroup>
        </div>
      </DsfrFieldset>
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="hasDeclarations">
      <InstructionDeclarationsTable :data="data" @open="openDeclaration" />
    </div>
    <p v-else class="mb-8">Il n'y a pas encore de déclarations.</p>
    <DsfrPagination
      v-if="showPagination"
      @update:currentPage="updatePage"
      :pages="pages"
      :current-page="page - 1"
      :truncLimit="5"
    />
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { computed, watch } from "vue"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import InstructionDeclarationsTable from "./InstructionDeclarationsTable"
import { DsfrPagination } from "@gouvminint/vue-dsfr"
import { useRoute, useRouter } from "vue-router"
import { getPagesForPagination } from "@/utils/components"
import { DsfrInput } from "@gouvminint/vue-dsfr"

const router = useRouter()
const route = useRoute()

const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)

const limit = 10
const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const pages = computed(() => getPagesForPagination(data.value.count, limit, route.path))

// Obtention de la donnée via API
const offset = computed(() => (page.value - 1) * limit)
const url = computed(
  () => `/api/v1/declarations/?limit=${limit}&offset=${offset.value}&status=${filteredStatus.value || ""}`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}
watch(page, fetchSearchResults)
watch(filteredStatus, fetchSearchResults)

const openDeclaration = (id) => router.push({ name: "InstructionPage", params: { declarationId: id } })

const statusFilterOptions = [
  { value: "", text: "Tous les statuts" },
  { value: "AWAITING_INSTRUCTION", text: "En attente d'instruction" },
  { value: "AWAITING_PRODUCER", text: "En attente de retour du producteur" },
  { value: "REJECTED", text: "Rejeté" },
  { value: "APPROVED", text: "Validé" },
]

const updateStatusFilter = (status) => router.push({ query: { ...route.query, ...{ status } } })
const updatePage = (newPage) => router.push({ query: { ...route.query, ...{ page: newPage + 1 } } })
</script>

<style scoped>
.filters :deep(legend.fr-fieldset__legend) {
  @apply pb-0 pt-4;
}
.filters :deep(.fr-input-group) {
  @apply mb-0 mt-2;
}
</style>
