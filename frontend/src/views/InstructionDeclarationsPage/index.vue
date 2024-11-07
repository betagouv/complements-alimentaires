<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Déclarations pour instruction' }]"
    />
    <div class="border px-4 mb-2 md:flex gap-4 items-baseline filters">
      <DsfrFieldset legend="Nom d'entreprise" class="!mb-0 min-w-44">
        <div class="flex gap-4">
          <DsfrInputGroup>
            <DsfrInput
              class="max-w-16 !text-sm"
              label="De :"
              :modelValue="companyNameStart"
              label-visible
              @update:modelValue="updateCompanyNameStartFilter"
            />
          </DsfrInputGroup>
          <DsfrInputGroup>
            <DsfrInput
              class="max-w-16 !text-sm"
              label="À :"
              :modelValue="companyNameEnd"
              label-visible
              @update:modelValue="updateCompanyNameEndFilter"
            />
          </DsfrInputGroup>
        </div>
      </DsfrFieldset>
      <div class="min-w-52">
        <DsfrFieldset class="!mb-0">
          <div class="md:border-x md:px-4">
            <DsfrInputGroup>
              <DsfrSelect
                label="Personne assignée"
                :modelValue="assignedInstructor"
                @update:modelValue="updateInstructorFilter"
                defaultUnselectedText=""
                :options="instructorSelectOptions"
                class="!text-sm"
              />
            </DsfrInputGroup>
          </div>
        </DsfrFieldset>
      </div>
      <StatusFilter :exclude="['DRAFT']" @updateFilter="updateStatusFilter" v-model="filteredStatus" />
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

          <DsfrInputGroup class="max-w-sm">
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

        <div class="md:border-l md:pl-4 min-w-36 pb-2">
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
import { computed, watch } from "vue"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import InstructionDeclarationsTable from "./InstructionDeclarationsTable"
import { useRoute, useRouter } from "vue-router"
import { getPagesForPagination } from "@/utils/components"
import { DsfrInput } from "@gouvminint/vue-dsfr"
import StatusFilter from "@/components/StatusFilter.vue"
import { orderingOptions, articleOptions } from "@/utils/mappings"
import PaginationSizeSelect from "@/components/PaginationSizeSelect"

const router = useRouter()
const route = useRoute()

const articleSelectOptions = [...articleOptions, ...[{ value: "", text: "Tous" }]]

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
    `/api/v1/declarations/?limit=${limit.value}&offset=${offset.value}&status=${filteredStatus.value || ""}&company_name_start=${companyNameStart.value}&company_name_end=${companyNameEnd.value}&ordering=${ordering.value}&instructor=${assignedInstructor.value}&article=${article.value}`
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
