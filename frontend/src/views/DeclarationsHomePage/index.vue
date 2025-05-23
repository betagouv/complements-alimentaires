<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Mes déclarations' }]"
    />
    <div class="block sm:flex items-center mb-8">
      <DsfrButton
        size="small"
        v-if="hasDeclarations"
        label="Nouvelle déclaration"
        secondary
        @click="createNewDeclaration"
      />
    </div>

    <HistoryAlert />

    <div class="border px-4 pt-4 mb-2 sm:flex gap-8 items-baseline filters">
      <DsfrFieldset class="mb-0!">
        <div class="md:pl-4">
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
        <div class="md:border-x md:px-4 min-w-44">
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
      <div class="md:border-r md:pr-4 min-w-48">
        <PaginationSizeSelect :modelValue="limit" @update:modelValue="updateLimit" />
      </div>
      <StatusFilter
        class="max-w-lg"
        @updateFilter="updateStatusFilter"
        :statusString="filteredStatus"
        :groupInstruction="true"
      />
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <DeclarationsTable :data="data" v-else-if="hasDeclarations" />
    <div v-else class="mb-8">
      <p>Vous n'avez pas encore des déclarations avec ces filtres.</p>
      <DsfrButton icon="ri-capsule-fill" label="Créer ma première déclaration" @click="createNewDeclaration" />
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
import { computed, watch } from "vue"
import ProgressSpinner from "@/components/ProgressSpinner"
import { handleError } from "@/utils/error-handling"
import DeclarationsTable from "./DeclarationsTable"
import { useRouter, useRoute } from "vue-router"
import { useFetch } from "@vueuse/core"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { getPagesForPagination } from "@/utils/components"
import PaginationSizeSelect from "@/components/PaginationSizeSelect"
import StatusFilter from "@/components/StatusFilter"
import HistoryAlert from "@/components/History/HistoryAlert.vue"

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
const router = useRouter()
const route = useRoute()
const company = computed(() => (route.query.company ? parseInt(route.query.company) : ""))
const author = computed(() => (route.query.author ? parseInt(route.query.author) : ""))

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

const createNewDeclaration = () => router.push({ name: "NewDeclaration" })

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })
const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateCompany = (newValue) => updateQuery({ company: newValue })
const updateAuthor = (newValue) => updateQuery({ author: newValue })
const updateLimit = (newValue) => updateQuery({ limit: newValue, page: 1 })

const url = computed(() => {
  let statusQuery = filteredStatus.value
  if (filteredStatus.value?.indexOf("INSTRUCTION") > -1)
    statusQuery += `${statusQuery.length ? "," : ""}AWAITING_INSTRUCTION,ONGOING_INSTRUCTION,AWAITING_VISA,ONGOING_VISA`
  return `/api/v1/users/${loggedUser.value.id}/declarations/?limit=${limit.value}&offset=${offset.value}&status=${statusQuery || ""}&ordering=-modificationDate&company=${company.value}&author=${author.value}`
})
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

watch([page, filteredStatus, company, author, limit], fetchSearchResults)
</script>
