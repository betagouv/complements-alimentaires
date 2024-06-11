<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { text: `Les déclarations de l'entreprise ${company.socialName}` },
      ]"
    />
    <div class="border px-4 pb-4 mb-2 sm:flex gap-8 items-baseline filters">
      <DsfrInputGroup>
        <DsfrSelect
          :modelValue="filteredStatus"
          label="Filtrer par statut"
          :options="statusFilterOptions"
          @update:modelValue="updateStatusFilter"
        />
      </DsfrInputGroup>
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="hasDeclarations">
      <CompanyDeclarationsTable :data="data" />
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
import { storeToRefs } from "pinia"
import { useRootStore } from "@/stores/root"
import { computed, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import CompanyDeclarationsTable from "./CompanyDeclarationsTable"
import ProgressSpinner from "@/components/ProgressSpinner"
import { statusFilterOptions } from "@/utils/mappings"

const route = useRoute()
const store = useRootStore()
const router = useRouter()
const { loggedUser, companies } = storeToRefs(store)
const company = computed(() => companies.value?.find((c) => +c.id === +route.params.id))

const limit = 10
const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit)

// Valeurs obtenus du queryparams
const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })
const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })

const url = computed(
  () =>
    `/api/v1/companies/${company.value?.id}/declarations/?&limit=${limit}&offset=${offset.value}&status=${filteredStatus.value || ""}`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

watch([page, filteredStatus], fetchSearchResults)
</script>
