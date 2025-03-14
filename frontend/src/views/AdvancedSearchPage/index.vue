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
                    :modelValue="article"
                    @update:modelValue="updateArticle"
                    :options="articleSelectOptions"
                    class="!text-sm"
                  />
                </DsfrInputGroup>
                <DsfrInputGroup>
                  <DsfrSelect
                    label="Population à risque"
                    defaultUnselectedText=""
                    :modelValue="article"
                    @update:modelValue="updateArticle"
                    :options="articleSelectOptions"
                    class="!text-sm"
                  />
                </DsfrInputGroup>
              </DsfrFieldset>
              <DsfrFieldset legend="Format" class="!mb-0 min-w-60">
                <DsfrInputGroup>
                  <DsfrSelect
                    label="Forme galénique"
                    defaultUnselectedText=""
                    :modelValue="article"
                    @update:modelValue="updateArticle"
                    :options="articleSelectOptions"
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
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { orderingOptions, articleOptionsWith15Subtypes } from "@/utils/mappings"
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

const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

// Valeurs obtenus du queryparams
const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const companyNameStart = computed(() => route.query.entrepriseDe)
const companyNameEnd = computed(() => route.query.entrepriseA)
const ordering = computed(() => route.query.triage)
const article = computed(() => route.query.article)
const limit = computed(() => route.query.limit)

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })

const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateCompanyNameStartFilter = (newValue) => updateQuery({ entrepriseDe: newValue })
const updateCompanyNameEndFilter = (newValue) => updateQuery({ entrepriseA: newValue })
const updateOrdering = (newValue) => updateQuery({ triage: newValue })
const updateArticle = (newValue) => updateQuery({ article: newValue })
const updateLimit = (newValue) => updateQuery({ limit: newValue, page: 1 })

const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit.value)

// Requêtes
const url = computed(
  () =>
    `/api/v1/declarations/?limit=${limit.value}&offset=${offset.value}&status=${filteredStatus.value || ""}&company_name_start=${companyNameStart.value}&company_name_end=${companyNameEnd.value}&ordering=${ordering.value}&article=${article.value}&search=${searchTerm.value}`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()

// Infos dans les champ
const articleSelectOptions = [...articleOptionsWith15Subtypes, ...[{ value: "", text: "Tous" }]]
</script>

<style scoped>
.search-area :deep(.fr-select-group) {
  @apply !my-0;
}
</style>
