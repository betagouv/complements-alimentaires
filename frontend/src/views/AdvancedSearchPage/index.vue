<template>
  <div :class="{ 'fr-container': true, seeOverflow }">
    <DsfrBreadcrumb
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Recherche avancée' }]"
    />
    <div class="mb-2 md:flex gap-16 search-area">
      <div class="md:w-2/4 pt-1">
        <DsfrFieldset legend="Recherche" class="!mb-0">
          <DsfrSearchBar v-model="searchTerm" placeholder="Nom du produit, ID ou entreprise" @search="search" />
        </DsfrFieldset>
      </div>
      <div class="md:w-2/4 md:flex gap-4">
        <DsfrInputGroup>
          <DsfrSelect
            label="Trier par"
            defaultUnselectedText=""
            :modelValue="ordering"
            @update:modelValue="updateOrdering"
            :options="orderingOptions"
            class="!text-sm"
          />
        </DsfrInputGroup>
        <PaginationSizeSelect :modelValue="limit" @update:modelValue="updateLimit" />
      </div>
    </div>
    <DsfrAccordionsGroup v-model="activeAccordion" class="border mb-8 filter-area">
      <DsfrAccordion id="filter-accordeon">
        <template v-slot:title>
          <p>
            <v-icon name="ri-equalizer-fill"></v-icon>
            Filtres
          </p>
        </template>
        <div>
          <div class="md:flex gap-16">
            <div class="md:w-2/4">
              <DsfrFieldset legend="Cible" class="min-w-60">
                <DsfrInputGroup>
                  <DsfrSelect
                    label="Population cible"
                    defaultUnselectedText=""
                    :modelValue="population"
                    @update:modelValue="updatePopulation"
                    :options="populationOptions"
                    class="!text-sm"
                  />
                </DsfrInputGroup>
                <DsfrInputGroup>
                  <DsfrSelect
                    label="Population à risque"
                    defaultUnselectedText=""
                    :modelValue="condition"
                    @update:modelValue="updateCondition"
                    :options="conditionOptions"
                    class="!text-sm"
                  />
                </DsfrInputGroup>
              </DsfrFieldset>
              <DsfrFieldset legend="Format" class="min-w-60">
                <DsfrInputGroup>
                  <DsfrSelect
                    label="Forme galénique"
                    defaultUnselectedText=""
                    :modelValue="galenicFormulation"
                    @update:modelValue="updateGalenicFormulation"
                    :options="galenicFormulationOptions"
                    class="!text-sm"
                  />
                </DsfrInputGroup>
              </DsfrFieldset>
            </div>
            <div class="md:w-2/4">
              <StatusFilter :exclude="['DRAFT']" @updateFilter="updateStatusFilter" :statusString="filteredStatus" />

              <DsfrInputGroup>
                <DsfrSelect
                  label="Article"
                  defaultUnselectedText=""
                  :modelValue="article"
                  @update:modelValue="updateArticle"
                  :options="articleSelectOptions"
                  class="!text-sm"
                />
              </DsfrInputGroup>

              <ElementAutocomplete
                v-model="ingredientSearchTerm"
                label="Composition"
                label-visible
                hint="Tapez au moins trois caractères pour démarrer la recherche. Les résultats contiendront tous les ingrédients ajoutés dans ce filtre."
                @selected="addIngredient"
                :hideSearchButton="true"
                :required="false"
                :chooseFirstAsDefault="false"
              />
              <div class="mt-2">
                <DsfrTag
                  v-for="([id, name, type], idx) in ingredientsToFilter"
                  :key="`ingredient-${id}`"
                  class="m-1 fr-tag--dismiss"
                  @click="removeIngredient(idx)"
                  :aria-label="`Retirer ${name}`"
                  tagName="button"
                >
                  <v-icon scale="0.85" class="mr-1" :name="getTypeIcon(type)" :aria-label="getTypeInFrench(type)" />
                  {{ name }}
                </DsfrTag>
              </div>
            </div>
          </div>
        </div>
      </DsfrAccordion>
    </DsfrAccordionsGroup>

    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="hasDeclarations">
      <SearchResultsTable :data="data" />
      <DsfrPagination
        v-if="showPagination"
        @update:currentPage="updatePage"
        :pages="pages"
        :current-page="page - 1"
        :truncLimit="5"
      />
    </div>
    <div v-else class="h-40 sm:h-60 rounded bg-slate-100 mb-8 flex flex-col items-center content-center justify-center">
      <v-icon scale="1.5" name="ri-archive-2-line"></v-icon>
      <p class="max-w-sm text-center mt-2">Nous n'avons pas trouvé des déclarations avec ces paramètres</p>
    </div>
  </div>
</template>
<script setup>
import { computed, ref, watch } from "vue"
import { storeToRefs } from "pinia"
import { useRoute, useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import ProgressSpinner from "@/components/ProgressSpinner"
import { articleOptionsWith15Subtypes } from "@/utils/mappings"
import { handleError } from "@/utils/error-handling"
import StatusFilter from "@/components/StatusFilter"
import PaginationSizeSelect from "@/components/PaginationSizeSelect"
import { getPagesForPagination } from "@/utils/components"
import SearchResultsTable from "./SearchResultsTable"
import { useRootStore } from "@/stores/root"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import { getTypeIcon, getTypeInFrench, typesMapping } from "@/utils/mappings"

const store = useRootStore()
store.fetchDeclarationFieldsData()

const router = useRouter()
const route = useRoute()
const searchTerm = ref(route.query.recherche)
const activeAccordion = ref()

// Valeurs obtenus du queryparams

const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const ordering = computed(() => route.query.triage)
const article = computed(() => route.query.article)
const population = computed(() => (route.query.population ? parseInt(route.query.population) : ""))
const condition = computed(() => (route.query.condition ? parseInt(route.query.condition) : ""))
const galenicFormulation = computed(() =>
  route.query.galenicFormulation ? parseInt(route.query.galenicFormulation) : ""
)
const limit = computed(() => route.query.limit)

// Mises à jour de la requête lors des changements des filtres et recherche

const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...{ page: 1 }, ...newQuery } })

const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateOrdering = (newValue) => updateQuery({ triage: newValue })
const updateArticle = (newValue) => updateQuery({ article: newValue })
const updatePopulation = (newValue) => updateQuery({ population: newValue })
const updateCondition = (newValue) => updateQuery({ condition: newValue })
const updateGalenicFormulation = (newValue) => updateQuery({ galenicFormulation: newValue })
const updateLimit = (newValue) => updateQuery({ limit: newValue })
const updateComposition = () =>
  updateQuery({ composition: ingredientsToFilter.value.map((x) => x.join("||")).join("|||") })

const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit.value)

const search = () => {
  updateQuery({ recherche: searchTerm.value })
  fetchSearchResults()
}

// Pagination

const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

// Filtre composition
// À noter qu'on utilise "||" et "|||" comme séparateurs dans l'URL pour ne pas entrer en conflit avec
// les noms d'ingrédients. Par exemple, une plante avec un ID: 12 et nom: Fraise serait codifiée
// dans le URL : `composition=12||Fraise||plant`. Le triple pipe "|||" sépare chaque élément.
const ingredientSearchTerm = ref()
const ingredientsToFilter = computed(() => {
  if (route.query.composition)
    return route.query.composition
      .split("|||")
      .map((x) => x?.split("||"))
      .filter((x) => x?.[2] && x[2] in typesMapping)
  return []
})
const addIngredient = (x) => {
  ingredientsToFilter.value.push([x.id, x.name, x.objectType])
  updateComposition()
}
const removeIngredient = (idx) => {
  ingredientsToFilter.value.splice(idx, 1)
  updateComposition()
}
const getApiUrlIdsForType = (types) => {
  const ids =
    ingredientsToFilter.value
      ?.filter((x) => types.indexOf(x[2]) > -1)
      .map((x) => x[0])
      .join(",") || []
  return ids.length ? ids : null
}

// Requêtes

const url = computed(() => {
  const baseUrl = "/api/v1/declarations"
  const limitQuery = limit.value ? `?limit=${limit.value}` : "?"
  const offsetQuery = offset.value ? `&offset=${offset.value}` : ""
  const statusQuery = filteredStatus.value ? `&status=${filteredStatus.value}` : ""
  const orderingQuery = ordering.value ? `&ordering=${ordering.value}` : ""
  const articleQuery = article.value ? `&article=${article.value}` : ""
  const populationQuery = population.value ? `&population=${population.value}` : ""
  const conditionQuery = condition.value ? `&condition=${condition.value}` : ""
  const galenicFormulationQuery = galenicFormulation.value ? `&galenic_formulation=${galenicFormulation.value}` : ""
  const searchQuery = searchTerm.value ? `&search=${searchTerm.value}` : ""

  const plantIds = getApiUrlIdsForType(["plant"])
  const microorganismIds = getApiUrlIdsForType(["microorganism"])
  const substanceIds = getApiUrlIdsForType(["substance"])
  const ingredientsIds = getApiUrlIdsForType([
    "ingredient",
    "form_of_supply",
    "aroma",
    "additive",
    "active_ingredient",
    "non_active_ingredient",
  ])

  const plantsQuery = plantIds ? `&plants=${plantIds}` : ""
  const microorganismsQuery = microorganismIds ? `&microorganisms=${microorganismIds}` : ""
  const substancesQuery = substanceIds ? `&substances=${substanceIds}` : ""
  const ingredientsQuery = ingredientsIds ? `&ingredients=${ingredientsIds}` : ""

  const fullPath = `${baseUrl}/${limitQuery}${offsetQuery}${statusQuery}${orderingQuery}${articleQuery}${populationQuery}${conditionQuery}${galenicFormulationQuery}${searchQuery}${plantsQuery}${microorganismsQuery}${substancesQuery}${ingredientsQuery}`

  // Enlève les `&` consecutifs
  return fullPath.replace(/&+/g, "&").replace(/&$/, "")
})
const { response, data, isFetching, execute } = useFetch(url).get().json()

const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

watch(
  [page, filteredStatus, ordering, article, limit, population, condition, galenicFormulation, ingredientsToFilter],
  fetchSearchResults
)

// Remplissage d'options dans les champs select

const { populations, conditions, galenicFormulations } = storeToRefs(store)
const toOptions = (list) => {
  const options =
    (list || [])
      .map((x) => ({ value: x.id, text: x.name.split(" (à préciser)")[0] })) // Transforme la réponse API en options pour les champs select
      .sort((a, b) => a.text.localeCompare(b.text)) || [] // Triage alphabétique
  options.unshift({ disabled: true, text: "---------" })
  options.unshift({ value: "", text: "Tout afficher" })
  return options
}

const articleSelectOptions = [
  ...[
    { value: "", text: "Tout afficher" },
    { disabled: true, text: "---------" },
  ],
  ...articleOptionsWith15Subtypes,
]
const orderingOptions = [
  { value: "name", text: "Nom du produit" },
  { value: "-name", text: "Nom du produit (descendant)" },
  { value: "creationDate", text: "Date de creation" },
  { value: "-creationDate", text: "Date de creation (descendant)" },
  { value: "modificationDate", text: "Date de modification" },
  { value: "-modificationDate", text: "Date de modification (descendant)" },
]
const populationOptions = computed(() => toOptions(populations.value))
const conditionOptions = computed(() => toOptions(conditions.value))
const galenicFormulationOptions = computed(() => toOptions(galenicFormulations.value))

// Petit hack pour l'animation de l'accordéon : Pour faire en sorte que le dropdown de
// ElementSearch soit visible en dehors de l'accordéon, on doit mettre `overflow:visible`
// (fait dans le CSS ci-dessous). Par contre, il faut appliquer un petit delai de 500ms
// pour permettre l'animation de se dérouler sans glitch visuel (la valeur de 500ms vient de
// https://github.com/GouvernementFR/dsfr/blob/0509e5697239ce12715cc0fcf0f5a69b0033ac6c/src/dsfr/core/script/collapse/collapse.js#L58
const seeOverflow = ref(false)
watch(activeAccordion, (x) => setTimeout(() => (seeOverflow.value = x === 0), 500))
///////////
</script>

<style scoped>
.search-area :deep(.fr-select-group) {
  @apply !my-0;
}
.filter-area :deep(.fr-fieldset__legend) {
  @apply !py-0;
}
.filter-area :deep(.fr-fieldset__element) {
  @apply !my-0;
}
div.seeOverflow :deep(#filter-accordeon.fr-collapse--expanded) {
  overflow: visible;
}
</style>
