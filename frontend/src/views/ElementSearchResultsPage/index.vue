<template>
  <div class="bg-blue-france-925 py-8">
    <div class="fr-container">
      <ElementAutocomplete
        v-model="searchTerm"
        label="Cherchez un ingrédient"
        hint="Tapez au moins trois caractères pour démarrer la recherche"
        @selected="goToSelectedOption"
        @search="search"
        :chooseFirstAsDefault="false"
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
      <DsfrAlert :title="calloutTitle" :description="calloutContent" type="info"></DsfrAlert>
    </div>
    <div v-else class="mb-4">
      <h1 class="fr-h3">Résultats de recherche</h1>
      <DsfrAlert :title="calloutTitle" :description="calloutContent" type="info" class="mb-5"></DsfrAlert>

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
import ElementAutocomplete from "@/components/ElementAutocomplete"
import { handleError } from "@/utils/error-handling"
import { slugifyType } from "@/utils/mappings"
import { getPagesForPagination } from "@/utils/components"

const router = useRouter()
const route = useRoute()
const searchTerm = ref(route.query.q || "")
const currentSearch = ref(route.query.q || "")
const calloutTitle = "Risque de non exhaustivité des données"
const calloutContent = `La base de données des ingrédients et substances constitue un guide sur lequel les opérateurs désireux de commercialiser des compléments alimentaires peuvent s’appuyer.
Cette base est en amélioration continue, l'équipe du BEPIAS et Compl'Alim font leur possible pour mettre à jour régulièrement et suivre la législation au plus proche.
Cependant et même si nous avons vocation à l'exhaustivité, il s’agit d’un outil administratif qui n'a pas force de loi.`

// Search
const search = (newTerm) => {
  if (newTerm.length < 3) window.alert("Veuillez saisir au moins trois caractères")
  else router.push({ query: { q: newTerm } })
}

// Pagination
const limit = 6
const page = ref(parseInt(route.query.page) || 1)
const offset = computed(() => (page.value - 1) * limit)
const showPagination = computed(() => data.value.count > limit)
const pages = computed(() => getPagesForPagination(data.value.count, limit, route.path))
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

const goToSelectedOption = (option) => {
  const slugguedType = slugifyType(option.objectType)
  const urlComponent = `${option?.id}--${slugguedType}--${option?.name}`
  return router.push({ name: "ElementPage", params: { urlComponent } })
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

<style scoped>
@reference "../../styles/index.css";

.fr-container :deep(input),
.fr-container :deep(button) {
  @apply mt-0!;
}
</style>
