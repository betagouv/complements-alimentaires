<template>
  <div>
    <DsfrNotice title="En construction" desc="Des nouvelles fonctionnalités arrivent bientôt !" />
    <div class="fr-container">
      <DsfrBreadcrumb
        class="mb-8"
        :links="[
          { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
          { text: 'Demandes d\'ajout d\'ingrédient' },
        ]"
      />
      <h1 class="fr-h4">Demandes d'ajout d'ingrédients</h1>
      <!-- <div class="border px-4 py-2 mb-2 md:flex gap-4 items-baseline filters">
      <div class="flex gap-4">
        <DsfrInputGroup>
          <DsfrInput
            class="!text-sm"
            label="Nom"
            :modelValue="name"
            label-visible
            @update:modelValue="updateNameFilter"
          />
        </DsfrInputGroup>
        <DsfrInputGroup>
          <DsfrSelect
            label="Type"
            :modelValue="type"
            @update:modelValue="updateTypeFilter"
            defaultUnselectedText=""
            :options="typeSelectOptions"
            class="!text-sm"
          />
        </DsfrInputGroup>
      </div>
      <div>
        <div class="md:border-l md:pl-4 min-w-36 flex flex-row gap-4">
          <DsfrInputGroup class="max-w-sm">
            <DsfrSelect
              label="Trier par"
              defaultUnselectedText=""
              :modelValue="ordering"
              @update:modelValue="updateOrdering"
              :options="orderingOptions"
              class="!text-sm"
            />
          </DsfrInputGroup>
          <PaginationSizeSelect :modelValue="limit" @update:modelValue="updateLimit" />
        </div>
      </div>
    </div> -->
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
import { useRoute, useRouter } from "vue-router"
import { getPagesForPagination } from "@/utils/components"
import { orderingOptions, typeOptions } from "@/utils/mappings"
import PaginationSizeSelect from "@/components/PaginationSizeSelect"

const router = useRouter()
const route = useRoute()

const typeSelectOptions = [...typeOptions, ...[{ value: "", text: "Tous" }]]

const hasRequests = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit.value)

const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

// Valeurs obtenus du queryparams
const page = computed(() => parseInt(route.query.page))
const name = computed(() => route.query.nom)
const type = computed(() => route.query.type)
const ordering = computed(() => route.query.triage)
const limit = computed(() => route.query.limit)

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })

const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateNameFilter = (newValue) => updateQuery({ nom: newValue })
const updateTypeFilter = (newValue) => updateQuery({ type: newValue })
const updateOrdering = (newValue) => updateQuery({ triage: newValue })
const updateLimit = (newValue) => updateQuery({ limit: newValue, page: 1 })

// Obtention de la donnée via API
const url = computed(
  () => `/api/v1/declared-elements/?limit=${limit.value}&offset=${offset.value}&name=${name.value}&type=${type.value}`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

watch([page, name, type, ordering, limit], fetchSearchResults)
</script>

<style scoped>
.filters :deep(legend.fr-fieldset__legend) {
  @apply pb-0 pt-4;
}
.filters :deep(.fr-input-group) {
  @apply mb-0 mt-2;
}
.filters :deep(.fr-select-group) {
  @apply mb-2;
}
</style>
