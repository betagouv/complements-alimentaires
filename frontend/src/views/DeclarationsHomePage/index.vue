<template>
  <TablePage
    :breadcrumbLinks="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Mes déclarations' }]"
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
          <PaginationSizeSelect :modelValue="limit" @update:modelValue="updateLimit" />
        </div>
        <div class="mb-1">
          <DsfrButton
            size="small"
            v-if="hasDeclarations"
            label="Nouvelle déclaration"
            secondary
            @click="createNewDeclaration"
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
          <StatusFilter @updateFilter="updateStatusFilter" :statusString="filteredStatus" :groupInstruction="true" />
        </div>
      </div>
    </template>
    <template v-slot:table>
      <DeclarationsTable :data="data" />
    </template>
    <template v-slot:no-results>
      <p>Vous n'avez pas encore des déclarations avec ces filtres.</p>
      <DsfrButton icon="ri-capsule-fill" label="Créer ma première déclaration" @click="createNewDeclaration" />
    </template>
  </TablePage>
</template>

<script setup>
import { computed, watch, ref } from "vue"
import { handleError } from "@/utils/error-handling"
import DeclarationsTable from "./DeclarationsTable"
import { useRouter, useRoute } from "vue-router"
import { useFetch } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { orderingOptionsPro } from "@/utils/mappings"
import PaginationSizeSelect from "@/components/PaginationSizeSelect"
import StatusFilter from "@/components/StatusFilter"
import TablePage from "@/components/TablePage"

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
const router = useRouter()
const route = useRoute()
const company = computed(() => (route.query.company ? parseInt(route.query.company) : ""))
const author = computed(() => (route.query.author ? parseInt(route.query.author) : ""))
const searchTerm = ref(route.query.recherche)
const ordering = computed(() => route.query.triage)

const hasDeclarations = computed(() => !!data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit.value)

const authorOptions = computed(() => {
  const allAuthors = data.value?.authors.map((x) => ({ value: x.id, text: `${x.firstName} ${x.lastName}` })) || []
  if ((data.value?.authors.map((x) => x.id) || []).indexOf(loggedUser.value.id) === -1)
    allAuthors.unshift({
      value: loggedUser.value.id,
      text: `${loggedUser.value.firstName} ${loggedUser.value.lastName}`,
    })
  const emptyOption = { value: "", text: "Toutes" }
  allAuthors.unshift(emptyOption)
  return allAuthors
})
const companiesOptions = computed(() => {
  const companies = loggedUser.value.companies?.map((x) => ({ value: x.id, text: x.socialName })) || []
  const emptyOption = { value: "", text: "Toutes" }
  companies.unshift(emptyOption)
  return companies
})

const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const limit = computed(() => route.query.limit)

const createNewDeclaration = () => router.push({ name: "NewDeclaration" })

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })
const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateCompany = (newValue) => updateQuery({ company: newValue })
const updateAuthor = (newValue) => updateQuery({ author: newValue })
const updateLimit = (newValue) => updateQuery({ limit: newValue, page: 1 })
const updateOrdering = (newValue) => updateQuery({ triage: newValue })

const url = computed(() => {
  let statusQuery = filteredStatus.value
  if (filteredStatus.value?.indexOf("INSTRUCTION") > -1)
    statusQuery += `${statusQuery.length ? "," : ""}AWAITING_INSTRUCTION,ONGOING_INSTRUCTION,AWAITING_VISA,ONGOING_VISA`
  return `/api/v1/users/${loggedUser.value.id}/declarations/?limit=${limit.value}&offset=${offset.value}&status=${statusQuery || ""}&ordering=-modificationDate&company=${company.value}&author=${author.value}&search=${searchTerm.value}&ordering=${ordering.value}`
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

watch([page, filteredStatus, company, author, limit, ordering], fetchSearchResults)
</script>
