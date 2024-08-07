<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Visa / Signature' }]"
    />
    <div class="border px-4 pt-4 mb-2 sm:flex gap-8 items-baseline filters">
      <StatusFilter
        :exclude="['DRAFT']"
        class="max-w-2xl"
        @update:modelValue="updateStatusFilter"
        v-model="filteredStatus"
      />
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="hasDeclarations">
      <VisaDeclarationsTable :data="data" />
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
import VisaDeclarationsTable from "./VisaDeclarationsTable"
import { useRoute, useRouter } from "vue-router"
import { getPagesForPagination } from "@/utils/components"
import StatusFilter from "@/components/StatusFilter.vue"

const router = useRouter()
const route = useRoute()

const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit)

const limit = 10
const pages = computed(() => getPagesForPagination(data.value.count, limit, route.path))

// Valeurs obtenus du queryparams
const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })

const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })

// Obtention de la donnée via API
const url = computed(
  () =>
    `/api/v1/declarations/?limit=${limit}&offset=${offset.value}&status=${filteredStatus.value || ""}&ordering=-modificationDate`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

watch([page, filteredStatus], fetchSearchResults)
</script>

<style scoped>
.filters :deep(legend.fr-fieldset__legend) {
  @apply pb-0 pt-4;
}
.filters :deep(.fr-input-group) {
  @apply mb-0 mt-2;
}
</style>
