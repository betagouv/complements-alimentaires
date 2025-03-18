<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Recherche avancée' }]"
    />
    <div class="mb-2 md:flex gap-16 search-area">
      <div class="md:w-2/4 pt-1">
        <DsfrFieldset legend="Recherche" class="!mb-0">
          <DsfrSearchBar v-model="searchTerm" placeholder="Nom du produit, ID ou entreprise" @search="search" />
        </DsfrFieldset>
      </div>
      <div class="md:w-2/4 md:flex gap-4">
        <DsfrInputGroup>
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
    <DsfrAccordionsGroup v-model="activeAccordion" class="border mb-8">
      <DsfrAccordion>
        <template v-slot:title>
          <p>
            <v-icon name="ri-equalizer-fill"></v-icon>
            Filtres
          </p>
        </template>
        <div>
          <div class="md:flex gap-16">
            <div class="md:w-2/4">
              <DsfrFieldset legend="Cible" class="!mb-0 min-w-60">
                <DsfrInputGroup>
                  <DsfrSelect
                    label="Population cible"
                    defaultUnselectedText=""
                    :modelValue="population"
                    @update:modelValue="updatePopulation"
                    :options="populationOptions"
                    class="!text-sm"
                  />
                </DsfrInputGroup>
                <DsfrInputGroup>
                  <DsfrSelect
                    label="Population à risque"
                    defaultUnselectedText=""
                    :modelValue="condition"
                    @update:modelValue="updateCondition"
                    :options="conditionOptions"
                    class="!text-sm"
                  />
                </DsfrInputGroup>
              </DsfrFieldset>
              <DsfrFieldset legend="Format" class="!mb-0 min-w-60">
                <DsfrInputGroup>
                  <DsfrSelect
                    label="Forme galénique"
                    defaultUnselectedText=""
                    :modelValue="galenicFormulation"
                    @update:modelValue="updateGalenicFormulation"
                    :options="galenicFormulationOptions"
                    class="!text-sm"
                  />
                </DsfrInputGroup>
              </DsfrFieldset>
            </div>
            <div class="md:w-2/4">
              <DsfrFieldset legend="Statut de la déclaration" class="!mb-0">
                <StatusFilter :exclude="['DRAFT']" @updateFilter="updateStatusFilter" :statusString="filteredStatus" />
              </DsfrFieldset>
              <DsfrInputGroup>
                <DsfrSelect
                  label="Article"
                  defaultUnselectedText=""
                  :modelValue="article"
                  @update:modelValue="updateArticle"
                  :options="articleSelectOptions"
                  class="!text-sm"
                />
              </DsfrInputGroup>
            </div>
          </div>
        </div>
      </DsfrAccordion>
    </DsfrAccordionsGroup>

    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="hasDeclarations">
      <SearchResultsTable :data="data" />
    </div>
    <div v-else class="h-40 sm:h-60 rounded bg-slate-100 mb-8 flex flex-col items-center content-center justify-center">
      <v-icon scale="1.5" name="ri-search-line"></v-icon>
      <p class="max-w-sm text-center mt-2">
        Effectuez votre recherche ou activez un des filtres pour voir les résultats
      </p>
      <DsfrButton size="sm" tertiary label="Afficher toutes les déclarations" @click="fetchSearchResults" />
    </div>
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
import { computed, ref, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import ProgressSpinner from "@/components/ProgressSpinner"
import { articleOptionsWith15Subtypes } from "@/utils/mappings"
import { handleError } from "@/utils/error-handling"
import StatusFilter from "@/components/StatusFilter"
import PaginationSizeSelect from "@/components/PaginationSizeSelect"
import { getPagesForPagination } from "@/utils/components"
import SearchResultsTable from "./SearchResultsTable"
import { useRootStore } from "@/stores/root"

const store = useRootStore()
store.fetchUnits()

const router = useRouter()
const route = useRoute()
const searchTerm = ref(route.query.recherche)
const activeAccordion = ref()

// Valeurs obtenus du queryparams

const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const ordering = computed(() => route.query.triage)
const article = computed(() => route.query.article)
const population = computed(() => route.query.population)
const condition = computed(() => route.query.condition)
const galenicFormulation = computed(() => route.query.galenicFormulation)
const limit = computed(() => route.query.limit)

// Mises à jour de la requête lors des changements des filtres et recherche

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })

const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateOrdering = (newValue) => updateQuery({ triage: newValue })
const updateArticle = (newValue) => updateQuery({ article: newValue })
const updatePopulation = (newValue) => updateQuery({ population: newValue })
const updateCondition = (newValue) => updateQuery({ condition: newValue })
const updateGalenicFormulation = (newValue) => updateQuery({ galenicFormulation: newValue })
const updateLimit = (newValue) => updateQuery({ limit: newValue, page: 1 })

const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit.value)

const search = () => {
  updateQuery({ recherche: searchTerm.value })
  fetchSearchResults()
}

// Pagination

const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

// Requêtes

const url = computed(
  () =>
    `/api/v1/declarations/?limit=${limit.value}&offset=${offset.value}&status=${filteredStatus.value || ""}&ordering=${ordering.value}&article=${article.value}&population=${population.value}&condition=${condition.value}&galenicFormulation=${galenicFormulation.value}&search=${searchTerm.value}`
)
const { response, data, isFetching, execute } = useFetch(url, { immediate: false }).get().json()

const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

watch([page, filteredStatus, ordering, article, limit, population, condition, galenicFormulation], fetchSearchResults)

// Infos dans les champs

const articleSelectOptions = [...articleOptionsWith15Subtypes, ...[{ value: "", text: "Tous" }]]
const orderingOptions = [
  { value: "name", text: "Nom du produit" },
  { value: "-name", text: "Nom du produit (descendant)" },
  { value: "creationDate", text: "Date de creation" },
  { value: "-creationDate", text: "Date de creation (descendant)" },
  { value: "modificationDate", text: "Date de modification" },
  { value: "-modificationDate", text: "Date de modification (descendant)" },
]
const populationOptions = []
const conditionOptions = []
const galenicFormulationOptions = []
</script>

<style scoped>
.search-area :deep(.fr-select-group) {
  @apply !my-0;
}
</style>
