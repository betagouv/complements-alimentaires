<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { text: 'Les déclarations de mon entreprise' },
      ]"
    />
    <HistoryAlert />

    <div class="border px-4 pt-4 pb-0 mb-2">
      <div class="md:pr-4 md:-mt-1 md:max-w-xl">
        <DsfrFieldset legend="Recherche" class="mb-0!">
          <DsfrSearchBar v-model="searchTerm" placeholder="Nom, ID ou entreprise" @search="search" />
        </DsfrFieldset>
      </div>
      <div class="sm:flex gap-8 items-baseline filters">
        <DsfrFieldset class="mb-0!">
          <div>
            <DsfrInputGroup>
              <DsfrSelect
                label="Entreprise"
                :modelValue="company"
                @update:modelValue="updateCompany"
                defaultUnselectedText="Toutes"
                :options="companiesOptions"
                class="text-sm!"
              />
            </DsfrInputGroup>
          </div>
        </DsfrFieldset>
        <DsfrFieldset class="mb-0!">
          <div class="md:border-x md:px-4">
            <DsfrInputGroup>
              <DsfrSelect
                label="Personne assignée"
                :modelValue="author"
                @update:modelValue="updateAuthor"
                defaultUnselectedText="Toutes"
                :options="authorOptions"
                class="text-sm!"
              />
            </DsfrInputGroup>
          </div>
        </DsfrFieldset>
        <StatusFilter
          :exclude="['DRAFT']"
          class="max-w-xl"
          @updateFilter="updateStatusFilter"
          :statusString="filteredStatus"
          :groupInstruction="true"
        />
      </div>
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="hasDeclarations">
      <CompanyDeclarationsTable :data="data" />
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
import { storeToRefs } from "pinia"
import { useRootStore } from "@/stores/root"
import { ref, computed, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import { getPagesForPagination } from "@/utils/components"
import CompanyDeclarationsTable from "./CompanyDeclarationsTable"
import ProgressSpinner from "@/components/ProgressSpinner"
import StatusFilter from "@/components/StatusFilter.vue"
import HistoryAlert from "@/components/History/HistoryAlert.vue"

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
const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit)

const pages = computed(() => getPagesForPagination(data.value.count, limit, route.path))

// Valeurs obtenus du queryparams
const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const company = computed(() => (route.query.company ? parseInt(route.query.company) : ""))
const author = computed(() => (route.query.author ? parseInt(route.query.author) : ""))

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })
const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateCompany = (newValue) => updateQuery({ company: newValue })
const updateAuthor = (newValue) => updateQuery({ author: newValue })

const url = computed(() => {
  let statusQuery = filteredStatus.value
  if (filteredStatus.value?.indexOf("INSTRUCTION") > -1)
    statusQuery += `${statusQuery.length ? "," : ""}AWAITING_INSTRUCTION,ONGOING_INSTRUCTION,AWAITING_VISA,ONGOING_VISA`
  return `/api/v1/users/${loggedUser.value.id}/declarations/?limit=${limit}&offset=${offset.value}&status=${statusQuery || ""}&ordering=-modificationDate&company=${company.value}&author=${author.value}&search=${searchTerm.value}`
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

watch([page, filteredStatus, company, author], fetchSearchResults)
</script>
