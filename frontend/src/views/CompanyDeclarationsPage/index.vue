<template>
  <TablePage
    :breadcrumbLinks="[
      { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
      { text: 'Les déclarations de mon entreprise' },
    ]"
    :data="data"
    :isFetching="isFetching"
    @updatePage="updatePage"
    :limit="limit"
    :route="route"
  >
    <template v-slot:primary>
      <div class="mb-2 md:flex gap-8 items-end">
        <div class="grow mb-4 sm:mb-0">
          <DsfrSearchBar
            v-model="searchTerm"
            label="Nom, ID ou entreprise"
            placeholder="Nom, ID ou entreprise"
            @search="search"
            @update:modelValue="(val) => val === '' && search()"
          />
        </div>
        <div class="sm:flex gap-3">
          <DsfrSelect
            label="Trier par"
            defaultUnselectedText=""
            :modelValue="ordering"
            @update:modelValue="updateOrdering"
            :options="orderingOptionsPro"
            class="text-sm!"
          />
        </div>
      </div>
    </template>
    <template v-slot:filter-box>
      <div class="grid sm:grid-cols-2">
        <div class="grid sm:grid-cols-2 gap-4 sm:pr-4 mb-4 sm:mb-0">
          <DsfrSelect
            label="Entreprise"
            :modelValue="company"
            @update:modelValue="updateCompany"
            defaultUnselectedText="Toutes"
            :options="companiesOptions"
            class="text-sm!"
          />
          <DsfrSelect
            label="Personne assignée"
            :modelValue="author"
            @update:modelValue="updateAuthor"
            defaultUnselectedText="Toutes"
            :options="authorOptions"
            class="text-sm!"
          />
        </div>
        <div class="sm:border-l sm:pl-4">
          <StatusFilter
            :exclude="['DRAFT']"
            @updateFilter="updateStatusFilter"
            :statusString="filteredStatus"
            :groupInstruction="true"
          />
        </div>
      </div>
    </template>
    <template v-slot:table>
      <CompanyDeclarationsTable :data="data" />
    </template>
    <template v-slot:no-results>
      <p class="mb-8">Aucune déclaration.</p>
    </template>
  </TablePage>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { storeToRefs } from "pinia"
import { useRootStore } from "@/stores/root"
import { ref, computed, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import CompanyDeclarationsTable from "./CompanyDeclarationsTable"
import StatusFilter from "@/components/StatusFilter.vue"
import { orderingOptionsPro } from "@/utils/mappings"
import TablePage from "@/components/TablePage.vue"

const route = useRoute()
const store = useRootStore()
const router = useRouter()
const { companies, loggedUser } = storeToRefs(store)
const searchTerm = ref(route.query.recherche)

const authorOptions = computed(() => {
  const allAuthors = data.value?.authors.map((x) => ({ value: x.id, text: `${x.firstName} ${x.lastName}` })) || []
  const emptyOption = { value: "", text: "Toutes" }
  allAuthors.unshift(emptyOption)
  return allAuthors
})
const companiesOptions = computed(() => {
  const allCompanies = companies.value?.map((x) => ({ value: x.id, text: x.socialName })) || []
  const emptyOption = { value: "", text: "Toutes" }
  allCompanies.unshift(emptyOption)
  return allCompanies
})

const limit = 10
const offset = computed(() => (page.value - 1) * limit)

// Valeurs obtenus du queryparams
const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const company = computed(() => (route.query.company ? parseInt(route.query.company) : ""))
const author = computed(() => (route.query.author ? parseInt(route.query.author) : ""))
const ordering = computed(() => route.query.triage)

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })
const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateCompany = (newValue) => updateQuery({ company: newValue })
const updateAuthor = (newValue) => updateQuery({ author: newValue })
const updateOrdering = (newValue) => updateQuery({ triage: newValue })

const url = computed(() => {
  let statusQuery = filteredStatus.value
  if (filteredStatus.value?.indexOf("INSTRUCTION") > -1)
    statusQuery += `${statusQuery.length ? "," : ""}AWAITING_INSTRUCTION,ONGOING_INSTRUCTION,AWAITING_VISA,ONGOING_VISA`
  return `/api/v1/users/${loggedUser.value.id}/declarations/?limit=${limit}&offset=${offset.value}&status=${statusQuery || ""}&ordering=-modificationDate&company=${company.value}&author=${author.value}&search=${searchTerm.value}&ordering=${ordering.value}`
})
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

const search = () => {
  updateQuery({ recherche: searchTerm.value })
  fetchSearchResults()
}

watch([page, filteredStatus, company, author, ordering], fetchSearchResults)
</script>
