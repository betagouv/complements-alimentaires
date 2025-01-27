<template>
  <div>
    <DsfrNotice title="En construction" desc="Des nouvelles fonctionnalités arrivent bientôt !" />
    <div class="fr-container">
      <DsfrBreadcrumb
        class="mb-8"
        :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Ingrédients pour ajout' }]"
      />
      <h1 class="fr-h4">Liste des demandes en attente d’ajout d’ingrédients</h1>
      <NewElementActionInfo />
      <div v-if="isFetching" class="flex justify-center my-10">
        <ProgressSpinner />
      </div>
      <div v-else-if="hasRequests">
        <NewElementsTable :data="data" />
      </div>
      <p v-else class="mb-8">Aucune demande.</p>
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
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import NewElementsTable from "./NewElementsTable"
import NewElementActionInfo from "./NewElementActionInfo"
import { useRoute, useRouter } from "vue-router"
import { getPagesForPagination } from "@/utils/components"

const router = useRouter()
const route = useRoute()

const hasRequests = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit.value)

const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

// Valeurs obtenus du queryparams
const page = computed(() => parseInt(route.query.page))
const name = computed(() => route.query.nom)
const type = computed(() => route.query.type)
const ordering = computed(() => route.query.triage)
const limit = computed(() => parseInt(route.query.limit) || 10)

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })

const updatePage = (newPage) => updateQuery({ page: newPage + 1 })

// Obtention de la donnée via API
const url = computed(
  () =>
    `/api/v1/new-declared-elements/?limit=${limit.value}&offset=${offset.value}&name=${name.value}&type=${type.value}`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

watch([page, name, type, ordering, limit], fetchSearchResults)
</script>
