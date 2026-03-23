<template>
  <div class="fr-container">
    <h1 class="sr-only">Mes déclarations</h1>
    <div class="md:grid md:grid-cols-5 lg:grid-cols-10 gap-3 items-end">
      <div class="col-span-5">
        <CaSearchBar
          v-model="searchTerm"
          label="Rechercher mes déclarations"
          placeholder="Nom, ID ou entreprise"
          label-visible
          @search="search"
        />
      </div>
      <div class="col-span-2">
        <div class="md:-my-6">
          <PaginationSizeSelect :modelValue="limit" @update:modelValue="updateLimit" />
        </div>
      </div>
      <div class="col-span-2">
        <DsfrSelect
          label="Trier par"
          defaultUnselectedText=""
          :modelValue="ordering"
          @update:modelValue="updateOrdering"
          :options="orderingOptionsPro"
          class="text-sm!"
        />
      </div>
      <p class="col-span-1 mb-0 mt-4 md:mt-0">
        <router-link
          v-if="hasDeclarations"
          :to="{ name: 'NewDeclaration' }"
          class="fr-btn fr-btn--secondary fr-btn--sm"
        >
          Nouvelle déclaration
        </router-link>
      </p>
    </div>
    <h2 class="fr-text--lg mt-4 mb-1">
      <v-icon name="ri-equalizer-fill"></v-icon>
      Filtres
    </h2>
    <div class="border px-4 mb-2 md:grid grid-cols-2 gap-4 items-center filters">
      <div class="md:border-r pr-4">
        <div class="sm:grid grid-cols-2 gap-4 items-baseline">
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
          <div class="min-w-44">
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
        </div>
      </div>
      <div class="py-2">
        <StatusFilter @updateFilter="updateStatusFilter" :statusString="filteredStatus" :groupInstruction="true" />
      </div>
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <DeclarationsTable :data="data" v-else-if="hasDeclarations" />
    <div v-else class="mb-8">
      <p>Vous n'avez pas encore des déclarations avec ces filtres.</p>
      <router-link :to="{ name: 'NewDeclaration' }" class="fr-btn">
        <v-icon name="ri-capsule-fill" class="mr-2"></v-icon>
        Créer ma première déclaration
      </router-link>
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
import { computed, watch, ref } from "vue"
import ProgressSpinner from "@/components/ProgressSpinner"
import { handleError } from "@/utils/error-handling"
import DeclarationsTable from "./DeclarationsTable"
import { useRouter, useRoute } from "vue-router"
import { useFetch } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { getPagesForPagination } from "@/utils/components"
import { orderingOptionsPro } from "@/utils/mappings"
import PaginationSizeSelect from "@/components/PaginationSizeSelect"
import StatusFilter from "@/components/StatusFilter"
import CaSearchBar from "@/components/CaSearchBar"
import { setDocumentTitle } from "@/utils/document"

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
const router = useRouter()
const route = useRoute()
const company = computed(() => (route.query.company ? parseInt(route.query.company) : ""))
const author = computed(() => (route.query.author ? parseInt(route.query.author) : ""))
const searchTerm = ref(route.query.recherche)
const ordering = computed(() => route.query.triage)

const hasDeclarations = computed(() => !!data.value?.results?.length)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
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

const pages = computed(() => getPagesForPagination(data.value.count, limit.value, route.path))

const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const limit = computed(() => route.query.limit)

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
  setDocumentTitle(["Mes déclarations"], {
    number: page.value,
    total: pages.value.length,
    term: "page",
  })
}

const search = () => {
  updateQuery({ recherche: searchTerm.value })
  fetchSearchResults()
}

watch([page, filteredStatus, company, author, limit, ordering], fetchSearchResults)
</script>

<style scoped>
@reference "../../styles/index.css";

.filters :deep(.fr-input-group) {
  @apply mb-0 mt-2;
}
.filters :deep(.fr-select-group) {
  @apply mb-2;
}
</style>
