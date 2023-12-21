<template>
  <div class="bg-blue-france-925 py-8">
    <div class="fr-container">
      <DsfrSearchBar />
    </div>
  </div>
  <div class="fr-container pb-6">
    <DsfrBreadcrumb class="mb-8" :links="[{ to: '/', text: 'Accueil' }, { text: `Recherche : « ${searchTerm} »` }]" />
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
</template>

<script setup>
import { onMounted, ref, computed } from "vue"
import { useRoute, onBeforeRouteUpdate } from "vue-router"
import { headers, verifyResponse } from "@/utils"
import ResultCard from "./ResultCard"

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

onBeforeRouteUpdate((to) => {
  if (!to.query?.q) return false
})
onMounted(() => {
  searchTerm.value = route.query.q
  loading.value = true
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
})
</script>
