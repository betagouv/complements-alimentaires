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
        @updateFilter="updateStatusFilter"
        :statusString="filteredStatus"
      />

      <div class="md:border-l md:pl-4">
        <DsfrInputGroup class="max-w-sm">
          <DsfrSelect
            label="Trier par"
            defaultUnselectedText=""
            :modelValue="ordering"
            @update:modelValue="updateOrdering"
            :options="orderingOptions"
          />
        </DsfrInputGroup>
      </div>
      <div class="md:border-l md:pl-4 min-w-48">
        <PaginationSizeSelect :modelValue="limit" @update:modelValue="updateLimit" />
      </div>
      <div class="md:border-l md:pl-4 min-w-36">
        <DsfrInputGroup class="max-w-sm">
          <DsfrSelect
            label="Article"
            defaultUnselectedText=""
            :modelValue="article"
            @update:modelValue="updateArticle"
            :options="articleSelectOptions"
            class="text-sm!"
          />
        </DsfrInputGroup>
      </div>
    </div>

    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="hasDeclarations">
      <VisaDeclarationsTable :data="data" />
    </div>
    <p v-else class="mb-8">Aucune déclaration.</p>
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
import StatusFilter from "@/components/StatusFilter"
import { orderingOptions, articleOptionsWith15Subtypes } from "@/utils/mappings"
import PaginationSizeSelect from "@/components/PaginationSizeSelect"
import { setDocumentTitle } from "@/utils/document"

const router = useRouter()
const route = useRoute()

const articleSelectOptions = [...articleOptionsWith15Subtypes, ...[{ value: "", text: "Tous" }]]

const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit.value)

const pages = computed(() => getPagesForPagination(data.value.count, limit.value, route.path))

// Valeurs obtenus du queryparams
const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const ordering = computed(() => route.query.triage)
const article = computed(() => route.query.article)
const limit = computed(() => route.query.limit)

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })

const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateOrdering = (newValue) => updateQuery({ triage: newValue })
const updateArticle = (newValue) => updateQuery({ article: newValue })
const updateLimit = (newValue) => updateQuery({ limit: newValue, page: 1 })

// Obtention de la donnée via API
const url = computed(
  () =>
    `/api/v1/declarations/?limit=${limit.value}&offset=${offset.value}&status=${filteredStatus.value || ""}&ordering=${ordering.value}&article=${article.value}`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
  setDocumentTitle(["Visa"], {
    number: page.value,
    total: pages.value.length,
    term: "page",
  })
}

watch([page, filteredStatus, ordering, article, limit], fetchSearchResults)
</script>

<style scoped>
@reference "../../styles/index.css";

.filters :deep(legend.fr-fieldset__legend) {
  @apply pb-0 pt-4;
}
.filters :deep(.fr-input-group) {
  @apply mb-0 mt-2;
}
</style>
