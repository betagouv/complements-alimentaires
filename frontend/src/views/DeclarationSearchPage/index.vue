<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { text: 'Recherche compléments alimentaires' },
      ]"
    />
    <h1 class="fr-h3">Tableau des compléments alimentaires</h1>
    <DsfrAlert title="Filtres en construction" />
    <ControlDeclarationsTable :data="data" v-if="data" />
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { computed, watch, ref } from "vue"
import { getPagesForPagination } from "@/utils/components"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import ControlDeclarationsTable from "./ControlDeclarationsTable"

const router = useRouter()
const route = useRoute()

const offset = computed(() => (page.value - 1) * limit.value)
const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

const page = computed(() => parseInt(route.query.page))
const limit = computed(() => route.query.limit)

// Obtention de la donnée via API
const url = computed(() => `/api/v1/control/declarations/?limit=${limit.value}&offset=${offset.value}`)
const { response, data, isFetching, execute } = useFetch(url).get().json()

const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}
</script>
