<template>
  <div>
    <DsfrNotice title="En construction" desc="Des nouvelles fonctionnalités arrivent bientôt !" />
    <div class="fr-container">
      <DsfrBreadcrumb
        class="mb-8"
        :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Ingrédients pour ajout' }]"
      />
      <h1 class="fr-h4">Liste des demandes en attente d’ajout d’ingrédients</h1>
      <router-link :to="{ name: 'CreateElement' }" class="fr-btn fr-btn--secondary fr-btn--sm mb-4">
        Créer un nouvel ingrédient
      </router-link>
      <NewElementActionInfo />
      <div class="border px-4 py-4 mb-2 sm:flex gap-8 items-baseline filters">
        <MultiselectFilter
          filterTitle="Statut de la demande :"
          :options="statusOptions"
          :selectedString="statusFilter"
          @updateFilter="(v) => updateQuery({ statut: v })"
          class="-mb-4 py-1"
        />
        <div class="md:border-l md:pl-4">
          <MultiselectFilter
            filterTitle="Statut de la déclaration :"
            :options="declarationStatusOptions"
            :selectedString="declarationStatusFilter"
            noFilterText="Toutes les déclarations ouvertes"
            @updateFilter="(v) => updateQuery({ statutDeclaration: v })"
            class="-mb-4 py-1"
          />
        </div>
      </div>
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
import { statusProps } from "@/utils/mappings"
import MultiselectFilter from "@/components/MultiselectFilter"

const router = useRouter()
const route = useRoute()

const hasRequests = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit.value)

const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

// Valeurs obtenus du queryparams
const page = computed(() => parseInt(route.query.page))
const statusFilter = computed(() => route.query.statut)
const declarationStatusFilter = computed(() => route.query.statutDeclaration)
const limit = computed(() => parseInt(route.query.limit) || 10)

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })

const updatePage = (newPage) => updateQuery({ page: newPage + 1 })

// Obtention de la donnée via API
const url = computed(
  () =>
    `/api/v1/new-declared-elements/?limit=${limit.value}&offset=${offset.value}&requestStatus=${statusFilter.value}&declarationStatus=${declarationStatusFilter.value}`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

watch([page, statusFilter, declarationStatusFilter, limit], fetchSearchResults)

const statusOptions = [
  { value: "REQUESTED", label: "Nouvelle" },
  { value: "INFORMATION", label: "Nécessite plus d'information", tagLabel: "Information" },
  { value: "REJECTED", label: "Refusé" },
  { value: "REPLACED", label: "Remplacé" },
]

const declarationStatuses = [
  "AWAITING_INSTRUCTION",
  "ONGOING_INSTRUCTION",
  "AWAITING_VISA",
  "ONGOING_VISA",
  "OBJECTION",
  "OBSERVATION",
  "AUTHORIZED",
  "ABANDONED",
  "REJECTED",
  "WITHDRAWN",
]
const declarationStatusOptions = declarationStatuses.map((key) => ({
  value: key,
  label: statusProps[key].label,
}))
</script>
