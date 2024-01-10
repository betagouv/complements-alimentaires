<template>
  <div class="bg-blue-france-925 py-8">
    <div class="fr-container">
      <DsfrSearchBar :placeholder="currentSearch" v-model="searchTerm" @search="search" />
    </div>
  </div>
  <div class="fr-container pb-6">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: '/', text: 'Accueil' }, { text: `Recherche : « ${currentSearch} »` }]"
    />
    <div v-if="emptyView">
      <h1 class="fr-h3">Nous n'avons pas trouvé des résultats pour « {{ currentSearch }} »</h1>
    </div>
    <div class="mb-4" v-else>
      <h1 class="fr-h3">Résultats de recherche</h1>
      <div v-if="visibleResults" class="grid grid-cols-12 gap-4">
        <ResultCard
          v-for="result in visibleResults"
          :key="result.id"
          class="col-span-12 sm:col-span-6 md:col-span-4"
          :result="result"
        />
      </div>
      <DsfrPagination
        class="mt-8"
        @update:currentPage="updatePage"
        :pages="pages"
        :current-page="page - 1"
        :truncLimit="5"
        v-if="showPagination"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue"
import { useRoute, useRouter, onBeforeRouteUpdate } from "vue-router"
import { headers, verifyResponse } from "@/utils"
import ResultCard from "./ResultCard"

let mounted = false
let currentSearch = ""

const router = useRouter()
const route = useRoute()
const searchTerm = ref(null)
const loading = ref(true)

// Pagination
const limit = 6
const page = ref(null)
const resultsCount = ref(null)
const offset = computed(() => (page.value - 1) * limit)
const showPagination = computed(() => resultsCount.value > limit)
const pages = computed(() => {
  const totalPages = Math.ceil(resultsCount.value / limit)
  const pages = []
  for (let i = 0; i < totalPages; i++)
    pages.push({
      label: i + 1,
      href: `${route.path}?page=${i + 1}`,
      title: `Page ${i + 1}`,
    })
  return pages
})
const updatePage = (newPage) => (page.value = newPage + 1)

// Results
const visibleResults = ref(null)
const emptyView = computed(() => !loading.value && resultsCount.value === 0)

const search = () => {
  if (searchTerm.value.length < 3) window.alert("Veuillez saisir au moins trois caractères")
  else router.push({ query: { q: searchTerm.value } })
}

const fetchSearchResults = () => {
  const url = "/api/v1/search/"
  const body = JSON.stringify({ search: currentSearch, limit, offset: offset.value })
  loading.value = true
  return fetch(url, { method: "POST", headers, body })
    .then(verifyResponse)
    .then((response) => {
      visibleResults.value = response.results
      resultsCount.value = response.count
    })
    .catch((e) => {
      window.alert("Une erreur est survenue veuillez réessayer plus tard")
      console.error(e)
    })
    .finally(() => (loading.value = false))
}

onBeforeRouteUpdate((to) => {
  if (!to.query?.q) return false
})

onMounted(() => {
  currentSearch = route.query.q
  page.value = route.query.page || 1
  fetchSearchResults().then(() => (mounted = true))
})

watch(
  () => route.query,
  () => {
    if (mounted) {
      currentSearch = route.query.q
      fetchSearchResults()
    }
  }
)

watch(page, () => {
  const routerFunction = route.query.page ? router.push : router.replace
  routerFunction({ query: { ...route.query, ...{ page: page.value } } })
})
</script>
