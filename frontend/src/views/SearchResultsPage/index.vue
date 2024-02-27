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
    <div v-else-if="isFinished && data.count === 0">
      <h1 class="fr-h3">Nous n'avons pas trouvé de résultats pour « {{ currentSearch }} »</h1>
    </div>
    <div v-else class="mb-4">
      <h1 class="fr-h3">Résultats de recherche</h1>
      <div v-if="isFinished && data.results" class="grid grid-cols-12 gap-4">
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
        v-if="isFinished && showPagination"
      />
    </div>
  </div>
</template>

<script setup>
// TODO: validation avec Vuelidate ?
// TODO: suspense à wrapper ailleurs ? warning single root
// TODO: le search component doit être le même sur ElementPage

import { ref, computed, watch } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import ResultCard from "./ResultCard"
import ProgressSpinner from "@/components/ProgressSpinner"
import useToaster from "@/composables/use-toaster"

const router = useRouter()
const route = useRoute()

// Search
const searchTerm = ref(route.query.q)
let currentSearch = ref(route.query.q)

const search = () => {
  currentSearch.value = searchTerm.value
  if (searchTerm.value.length < 3) {
    useToaster().addMessage({
      id: "search-result-missing-chars",
      type: "error",
      description: "Veuillez saisir au moins trois caractères",
    })
  } else {
    execute()
    if (error.value) useToaster().addUnknownErrorMessage()
  }
}

// Pagination
const limit = 6
const page = ref(route.query.page || 1)
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

// Search Request
const body = computed(() => ({ search: searchTerm.value, limit: limit, offset: offset.value }))
const { error, data, isFetching, isFinished, execute } = useFetch(
  "/api/v1/search/",
  { headers: headers },
  { immediate: false }
)
  .post(body)
  .json()

// Init
router.push({ query: { q: searchTerm.value } })
await search()

// Watcher for pagination

watch(page, async () => {
  const routerFunction = route.query.page ? router.push : router.replace
  routerFunction({ query: { ...route.query, ...{ page: page.value } } })
  await search()
})
</script>
