<template>
  <div class="bg-blue-france-925 py-8">
    <div class="fr-container">
      <DsfrSearchBar v-model="searchTerm" @search="search" />
    </div>
  </div>
  <div class="fr-container pb-6">
    <DsfrBreadcrumb class="mb-8" :links="[{ to: '/', text: 'Accueil' }, { text: `Recherche : « ${searchTerm} »` }]" />
    <div v-if="emptyView">
      <h1 class="fr-h3">Nous n'avons pas trouvé des résultats pour « {{ searchTerm }} »</h1>
    </div>
    <div v-else>
      <h1 class="fr-h3">Résultats de recherche</h1>
      <div v-if="visibleResults" class="grid grid-cols-12 gap-4">
        <ResultCard
          v-for="result in visibleResults"
          :key="result.id"
          class="col-span-12 sm:col-span-6 md:col-span-4"
          :result="result"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue"
import { useRoute, useRouter, onBeforeRouteUpdate } from "vue-router"
import { headers, verifyResponse } from "@/utils"
import ResultCard from "./ResultCard"

const router = useRouter()
const route = useRoute()
const searchTerm = ref(null)
const loading = ref(true)

// Pagination
const limit = 12
const page = ref(1) // TODO : proper page management
const resultsCount = ref(null)
const offset = computed(() => (page.value - 1) * limit)

// Results
const visibleResults = ref(null)
const emptyView = computed(() => !loading.value && resultsCount.value === 0)

const search = () => {
  // TODO : Limit to more than 3 chars
  router.push({ query: { q: searchTerm.value } })
}

const fetchSearchResults = () => {
  const url = "/api/v1/search/"
  const body = JSON.stringify({ search: searchTerm.value, limit, offset: offset.value })
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
  searchTerm.value = route.query.q
  loading.value = true
  return fetchSearchResults()
})

watch(() => route.query.q, fetchSearchResults)
</script>
