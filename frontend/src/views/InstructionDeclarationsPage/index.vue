<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Déclarations pour instruction' }]"
    />
    <div class="border px-4 mb-2 md:flex gap-4 items-baseline filters">
      <div>
        <div class="sm:flex gap-4 items-baseline md:border-r">
          <DsfrFieldset legend="Nom d'entreprise" class="mb-0! min-w-44">
            <div class="flex gap-4">
              <DsfrInputGroup>
                <DsfrInput
                  class="max-w-16 text-sm!"
                  label="De :"
                  :modelValue="companyNameStart"
                  label-visible
                  @update:modelValue="updateCompanyNameStartFilter"
                />
              </DsfrInputGroup>
              <DsfrInputGroup>
                <DsfrInput
                  class="max-w-16 text-sm!"
                  label="À :"
                  :modelValue="companyNameEnd"
                  label-visible
                  @update:modelValue="updateCompanyNameEndFilter"
                />
              </DsfrInputGroup>
            </div>
          </DsfrFieldset>
          <DsfrFieldset class="mb-0! min-w-52">
            <div class="md:px-4 md:border-l">
              <DsfrInputGroup>
                <DsfrSelect
                  label="Personne assignée"
                  :modelValue="assignedInstructor"
                  @update:modelValue="updateInstructorFilter"
                  defaultUnselectedText=""
                  :options="instructorSelectOptions"
                  class="text-sm!"
                />
              </DsfrInputGroup>
            </div>
          </DsfrFieldset>
        </div>
        <div class="md:pr-4 md:border-r md:border-t md:-mt-3">
          <DsfrFieldset legend="Recherche" class="mb-0!">
            <DsfrSearchBar
              v-model="searchTerm"
              label="Nom, ID ou entreprise"
              placeholder="Nom, ID ou entreprise"
              @search="search"
            />
          </DsfrFieldset>
        </div>
      </div>
      <StatusFilter :exclude="['DRAFT']" @updateFilter="updateStatusFilter" :statusString="filteredStatus" />
      <div class="min-w-96 md:border-l">
        <div class="md:pl-4 min-w-36 flex flex-row gap-4">
          <div class="w-2/4">
            <DsfrInputGroup>
              <DsfrSelect
                label="Trier par"
                defaultUnselectedText=""
                :modelValue="ordering"
                @update:modelValue="updateOrdering"
                :options="orderingOptions"
                class="text-sm!"
              />
            </DsfrInputGroup>
          </div>
          <div class="w-2/4">
            <DsfrInputGroup>
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

        <div class="md:pl-4 min-w-36 pb-2">
          <PaginationSizeSelect :modelValue="limit" @update:modelValue="updateLimit" />
        </div>
      </div>
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="hasDeclarations">
      <InstructionDeclarationsTable :data="data" />
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
import { computed, watch, ref } from "vue"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import InstructionDeclarationsTable from "./InstructionDeclarationsTable"
import { useRoute, useRouter } from "vue-router"
import { getPagesForPagination } from "@/utils/components"
import StatusFilter from "@/components/StatusFilter.vue"
import { orderingOptions, articleOptionsWith15Subtypes } from "@/utils/mappings"
import PaginationSizeSelect from "@/components/PaginationSizeSelect"

const router = useRouter()
const route = useRoute()
const searchTerm = ref(route.query.recherche)

const articleSelectOptions = [...articleOptionsWith15Subtypes, ...[{ value: "", text: "Tous" }]]

const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit.value)

const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))
const allInstructors = computed(() => data.value?.instructors)
const instructorSelectOptions = computed(() => {
  const availableInstructors = allInstructors.value?.map((x) => ({ value: "" + x.id, text: x.name })) || []
  availableInstructors.unshift({ value: "None", text: "Déclarations non assignées" })
  availableInstructors.unshift({ value: "", text: "Toutes les déclarations" })
  return availableInstructors
})

// Valeurs obtenus du queryparams
const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const companyNameStart = computed(() => route.query.entrepriseDe)
const companyNameEnd = computed(() => route.query.entrepriseA)
const assignedInstructor = computed(() => route.query.personneAssignée)
const ordering = computed(() => route.query.triage)
const article = computed(() => route.query.article)
const limit = computed(() => route.query.limit)

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })

const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateCompanyNameStartFilter = (newValue) => updateQuery({ entrepriseDe: newValue })
const updateCompanyNameEndFilter = (newValue) => updateQuery({ entrepriseA: newValue })
const updateInstructorFilter = (newValue) => updateQuery({ personneAssignée: newValue })
const updateOrdering = (newValue) => updateQuery({ triage: newValue })
const updateArticle = (newValue) => updateQuery({ article: newValue })
const updateLimit = (newValue) => updateQuery({ limit: newValue, page: 1 })

// Obtention de la donnée via API
const url = computed(
  () =>
    `/api/v1/declarations/?limit=${limit.value}&offset=${offset.value}&status=${filteredStatus.value || ""}&company_name_start=${companyNameStart.value}&company_name_end=${companyNameEnd.value}&ordering=${ordering.value}&instructor=${assignedInstructor.value}&article=${article.value}&search=${searchTerm.value}`
)
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

watch(
  [page, filteredStatus, companyNameStart, companyNameEnd, assignedInstructor, ordering, article, limit],
  fetchSearchResults
)

const search = () => {
  updateQuery({ recherche: searchTerm.value })
  fetchSearchResults()
}
</script>

<style scoped>
@reference "../../styles/index.css";

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
