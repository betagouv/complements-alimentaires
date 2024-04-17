<template>
  <div class="bg-blue-france-925 py-8">
    <div class="fr-container">
      <DsfrSearchBar
        placeholder="Rechercher par ingrédient, plante, substance..."
        v-model="searchTerm"
        @search="search"
      />
    </div>
  </div>
  <div class="fr-container pb-6">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: '/', text: 'Accueil' }, { text: `Recherche : « ${currentSearch} »` }]"
    />
    <div v-if="isFetching" class="flex justify-center my-24">
      <ProgressSpinner />
    </div>
    <div v-else-if="data.count === 0">
      <h1 class="fr-h3">Nous n'avons pas trouvé de résultats pour « {{ currentSearch }} »</h1>
      <DsfrAlert title="Non exhaustivité des données" :description="calloutContent" type="info"></DsfrAlert>
    </div>
    <div v-else class="mb-4">
      <h1 class="fr-h3">Résultats de recherche</h1>
      <DsfrAlert
        title="Non exhaustivité des données"
        :description="calloutContent"
        type="info"
        class="mb-5"
      ></DsfrAlert>

      <div v-if="data.results" class="grid grid-cols-12 gap-4">
        <ResultCard
          v-for="result in data.results"
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
import { ref, computed, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import ResultCard from "./ResultCard"
import ProgressSpinner from "@/components/ProgressSpinner"
import { handleError } from "@/utils/error-handling"
import { DsfrCallout } from "@gouvminint/vue-dsfr"

const router = useRouter()
const route = useRoute()
const searchTerm = ref(route.query.q || "")
const currentSearch = ref(route.query.q || "")
const calloutContent = `La base de données des ingrédients et substances constitue un guide sur lequel les opérateurs désireux de commercialiser des compléments alimentaires peuvent s’appuyer.
Cette base est en amélioration continue et vise à être mise à jour régulièrement pour suivre la législation au plus proche.
Cependant, il s’agit d’un outil administratif qui n'a pas force de loi.`

// Search
const search = () => {
  if (searchTerm.value.length < 3) window.alert("Veuillez saisir au moins trois caractères")
  else router.push({ query: { q: searchTerm.value } })
}

// Pagination
const limit = 6
const page = ref(parseInt(route.query.page) || 1)
const offset = computed(() => (page.value - 1) * limit)
const showPagination = computed(() => data.value.count > limit)
const pages = computed(() => {
  const totalPages = Math.ceil(data.value.count / limit)
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

// Search request
const body = computed(() => ({ search: currentSearch.value, limit: limit, offset: offset.value }))
const { data, response, isFetching, execute } = useFetch(
  "/api/v1/search/",
  { headers: headers() },
  { immediate: false }
)
  .post(body)
  .json()

const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

// Initial search
fetchSearchResults() // No need for Suspense

// Watchers
watch(
  () => route.query,
  () => {
    currentSearch.value = route.query.q
    fetchSearchResults()
  }
)

watch(page, () => {
  const routerFunction = route.query.page ? router.push : router.replace
  routerFunction({ query: { ...route.query, ...{ page: page.value } } })
})
</script>
