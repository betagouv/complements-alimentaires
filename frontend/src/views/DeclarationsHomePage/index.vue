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
    <div class="border px-4 pt-4 mb-2 sm:flex gap-8 items-baseline filters">
      <StatusFilter
        class="max-w-2xl"
        @updateFilter="updateStatusFilter"
        v-model="filteredStatus"
        :groupInstruction="true"
      />
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <DeclarationsTable :data="data" v-else-if="hasDeclarations" />
    <div v-else class="mb-8">
      <p>Vous n'avez pas encore créé des déclarations.</p>
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
import StatusFilter from "@/components/StatusFilter.vue"

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
const router = useRouter()
const route = useRoute()

const hasDeclarations = computed(() => !!data.value?.results?.length)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit)

const limit = 10
const pages = computed(() => getPagesForPagination(data.value.count, limit, route.path))

const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)

const createNewDeclaration = () => router.push({ name: "NewDeclaration" })

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...newQuery } })
const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })

const url = computed(() => {
  let statusQuery = filteredStatus.value
  if (filteredStatus.value?.indexOf("INSTRUCTION") > -1)
    statusQuery += `${statusQuery.length ? "," : ""}AWAITING_INSTRUCTION,ONGOING_INSTRUCTION,AWAITING_VISA,ONGOING_VISA`
  return `/api/v1/users/${loggedUser.value.id}/declarations/?limit=${limit}&offset=${offset.value}&status=${statusQuery || ""}&ordering=-modificationDate`
})
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

watch([page, filteredStatus], fetchSearchResults)
</script>
