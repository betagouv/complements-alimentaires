<template>
  <div class="fr-container pb-8">
    <DsfrBreadcrumb
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Recherche entreprises' }]"
    />
    <h1 class="fr-h3">Entreprises responsables de la mise sur le marché</h1>
    <DsfrAlert title="Recherche et filtrage avancé en construction" />
    <div v-if="isFetching && !data" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else>
      <ControlCompanyTable :data="data" v-if="data" @sort="updateOrdering" />
      <DsfrPagination
        v-if="showPagination"
        @update:currentPage="updatePage"
        :pages="pages"
        :current-page="page - 1"
        :truncLimit="5"
      />
    </div>
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { computed, watch } from "vue"
import { getPagesForPagination } from "@/utils/components"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import ControlCompanyTable from "./ControlCompanyTable"

const router = useRouter()
const route = useRoute()

const offset = computed(() => (page.value - 1) * limit.value)
const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

const page = computed(() => parseInt(route.query.page))
const ordering = computed(() => route.query.triage)
const limit = computed(() => parseInt(route.query.limit))
const showPagination = computed(() => data.value?.count > data.value?.results?.length)

// Obtention de la donnée via API
const url = computed(
  () => `/api/v1/control/companies/?limit=${limit.value}&offset=${offset.value}&ordering=${ordering.value}`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()

const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

// Mise à jour des paramètres
const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...{ page: 1 }, ...newQuery } })

const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateOrdering = (sortValue) => updateQuery({ triage: sortValue || "-creationDate" })

watch([page, limit, ordering], fetchSearchResults)
</script>
