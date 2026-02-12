<template>
  <TablePage
    :breadcrumbLinks="[
      { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
      { text: 'Déclarations pour instruction' },
    ]"
    :data="data"
    :isFetching="isFetching"
    @updatePage="updatePage"
    :limit="limit"
    :route="route"
  >
    <template v-slot:primary>
      <div class="mb-2 md:flex gap-8 items-end">
        <div class="grow">
          <DsfrSearchBar
            v-model="searchTerm"
            label="Nom, ID ou entreprise"
            placeholder="Nom, ID ou entreprise"
            @search="search"
          />
        </div>
        <div class="sm:flex gap-3">
          <DsfrSelect
            label="Trier par"
            defaultUnselectedText=""
            :modelValue="ordering"
            @update:modelValue="updateOrdering"
            :options="orderingOptions"
            class="text-sm!"
          />
          <PaginationSizeSelect :modelValue="limit" @update:modelValue="updateLimit" />
        </div>
      </div>
    </template>
    <template v-slot:filter-box>
      <div class="grid sm:grid-cols-2">
        <div class="flex gap-4 mb-4 sm:mb-0 sm:pr-4 items-baseline">
          <DsfrFieldset legend="Nom d'entreprise" class="min-w-44">
            <div class="flex gap-4">
              <div>
                <DsfrInput
                  class="max-w-16 text-sm!"
                  label="De :"
                  :modelValue="companyNameStart"
                  label-visible
                  @update:modelValue="updateCompanyNameStartFilter"
                />
              </div>
              <div>
                <DsfrInput
                  class="max-w-16 text-sm!"
                  label="À :"
                  :modelValue="companyNameEnd"
                  label-visible
                  @update:modelValue="updateCompanyNameEndFilter"
                />
              </div>
            </div>
          </DsfrFieldset>
          <DsfrSelect
            label="Personne assignée"
            :modelValue="assignedInstructor"
            @update:modelValue="updateInstructorFilter"
            defaultUnselectedText=""
            :options="instructorSelectOptions"
            class="text-sm!"
          />
          <DsfrSelect
            label="Article"
            defaultUnselectedText=""
            :modelValue="article"
            @update:modelValue="updateArticle"
            :options="articleSelectOptions"
            class="text-sm!"
          />
        </div>
        <div class="sm:border-l sm:pl-4">
          <StatusFilter :exclude="['DRAFT']" @updateFilter="updateStatusFilter" :statusString="filteredStatus" />
        </div>
      </div>
    </template>
    <template v-slot:table>
      <InstructionDeclarationsTable :data="data" />
    </template>
    <template v-slot:no-results>
      <p class="mb-8">Aucune déclaration.</p>
    </template>
  </TablePage>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { computed, watch, ref } from "vue"
import { handleError } from "@/utils/error-handling"
import InstructionDeclarationsTable from "./InstructionDeclarationsTable"
import { useRoute, useRouter } from "vue-router"
import StatusFilter from "@/components/StatusFilter.vue"
import { orderingOptions, articleOptionsWith15Subtypes } from "@/utils/mappings"
import PaginationSizeSelect from "@/components/PaginationSizeSelect"
import TablePage from "@/components/TablePage.vue"

const router = useRouter()
const route = useRoute()
const searchTerm = ref(route.query.recherche)

const articleSelectOptions = [...articleOptionsWith15Subtypes, ...[{ value: "", text: "Tous" }]]

const offset = computed(() => (page.value - 1) * limit.value)

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
