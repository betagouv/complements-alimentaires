<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: '/tableau-de-bord', text: 'Tableau de bord' }, { text: 'Toutes les déclarations' }]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <InstructionDeclarationsTable v-else-if="hasDeclarations" :data="data" @open="openDeclaration" />
    <p v-else class="mb-8">Il n'y a pas encore de déclarations.</p>
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
import { DsfrPagination } from "@gouvminint/vue-dsfr"
import { useRoute, useRouter } from "vue-router"
import { getPagesForPagination } from "@/utils/components"

const router = useRouter()
const route = useRoute()

const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)

const updatePage = (newPage) => router.push({ query: { page: newPage + 1 } })

const limit = 10
const page = computed(() => parseInt(route.query.page))
const pages = computed(() => getPagesForPagination(data.value.count, limit, route.path))

// Obtention de la donnée via API
const offset = computed(() => (page.value - 1) * limit)
const url = computed(() => `/api/v1/declarations/?limit=${limit}&offset=${offset.value}`)
const { response, data, isFetching, execute } = useFetch(url).get().json()
const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}
watch(page, fetchSearchResults)

const openDeclaration = (id) => router.push({ name: "InstructionPage", params: { declarationId: id } })
</script>
