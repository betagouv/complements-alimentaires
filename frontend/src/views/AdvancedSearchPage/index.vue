<template>
  <div :class="{ 'fr-container': true, seeOverflow }">
    <DsfrBreadcrumb
      :links="[{ to: { name: 'DashboardPage' }, text: 'Tableau de bord' }, { text: 'Recherche avancée' }]"
    />
    <div class="mb-2 md:flex gap-8 search-area">
      <div class="md:w-1/3 lg:w-2/5 pt-1">
        <DsfrFieldset legend="Recherche" class="mb-0!">
          <DsfrSearchBar
            v-model="searchTerm"
            label="Nom du produit, ID ou entreprise"
            placeholder="Nom du produit, ID ou entreprise"
            @search="search"
            @update:modelValue="(val) => val === '' && search()"
          />
        </DsfrFieldset>
      </div>
      <div class="md:w-2/3 lg:w-3/5 md:flex gap-3">
        <DsfrInputGroup>
          <DsfrSelect
            label="Trier par"
            defaultUnselectedText=""
            :modelValue="ordering"
            @update:modelValue="updateOrdering"
            :options="orderingOptions"
            class="text-sm!"
          />
        </DsfrInputGroup>
        <PaginationSizeSelect :modelValue="limit" @update:modelValue="updateLimit" />
        <div class="md:mt-6 justify-self-end shrink self-center">
          <DsfrButton @click="canDownloadFile ? null : (opened = true)" secondary size="sm" icon="ri-file-excel-2-fill">
            <a :href="canDownloadFile ? excelUrl : 'javascript:void(0)'" download>Télécharger</a>
          </DsfrButton>
          <DsfrModal v-model:opened="opened" title="Nombre de déclarations trop élévé" @close="opened = false">
            <p>
              La recherche actuelle présente {{ data?.count }} résultats. Un maximum de
              {{ maxDownloadSize }} déclarations peuvent être exportées.
            </p>
            <p>
              Merci d'affiner votre recherche ou de contacter notre équipe pour demander un export avec les filtres
              choisis.
            </p>
          </DsfrModal>
        </div>
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
              <StatusFilter
                :exclude="['DRAFT']"
                @updateFilter="updateStatusFilter"
                :statusString="filteredStatus"
                class="my-6 status-filter"
              />
              <DsfrFieldset legend="Cible" class="min-w-60">
                <DsfrInputGroup>
                  <DsfrSelect
                    label="Population cible"
                    defaultUnselectedText=""
                    :modelValue="population"
                    @update:modelValue="updatePopulation"
                    :options="populationOptions"
                    class="text-sm!"
                  />
                </DsfrInputGroup>
                <DsfrInputGroup>
                  <DsfrSelect
                    label="Population à risque"
                    defaultUnselectedText=""
                    :modelValue="condition"
                    @update:modelValue="updateCondition"
                    :options="conditionOptions"
                    class="text-sm!"
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
                    class="text-sm!"
                  />
                </DsfrInputGroup>
              </DsfrFieldset>
              <DsfrFieldset legend="Localisation" class="min-w-60">
                <DsfrInputGroup>
                  <CountryField :modelValue="country" @update:modelValue="updateCountry" :includeAllOption="true" />
                </DsfrInputGroup>
              </DsfrFieldset>
            </div>
            <div class="md:w-2/4">
              <DsfrInputGroup>
                <DsfrSelect
                  label="Article"
                  defaultUnselectedText=""
                  :modelValue="article"
                  @update:modelValue="updateArticle"
                  :options="articleSelectOptions"
                  class="text-sm!"
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
                :searchAll="true"
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
              <div class="mt-4">
                <label for="dose-filter" class="fr-label">Dose</label>
                <DoseFilterModal :modelValue="dose" @update:modelValue="updateDose" id="dose-filter" />
              </div>

              <div class="mt-8">
                <DsfrFieldset legend="Date de soumission" legendClass="fr-label font-medium!">
                  <div class="flex gap-4 mt-2">
                    <DateFilterField
                      :dateField="submissionDateAfter"
                      label="Après le"
                      :updateFn="updateSubmissionDateAfter"
                    />
                    <DateFilterField
                      :dateField="submissionDateBefore"
                      label="Avant le"
                      :updateFn="updateSubmissionDateBefore"
                    />
                  </div>
                </DsfrFieldset>
              </div>
              <div class="mt-8">
                <DsfrFieldset legend="Date de la prise de décision" legendClass="fr-label font-medium!">
                  <div class="flex gap-4 mt-2">
                    <DateFilterField
                      :dateField="decisionDateAfter"
                      label="Après le"
                      :updateFn="updateDecisionDateAfter"
                    />
                    <DateFilterField
                      :dateField="decisionDateBefore"
                      label="Avant le"
                      :updateFn="updateDecisionDateBefore"
                    />
                  </div>
                </DsfrFieldset>
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
      <div class="text-right">
        <p class="text-sm! -mb-2 -mt-4 font-medium" aria-live="polite">
          {{ data.count }} {{ data.count === 1 ? "résultat" : "résultats" }}
        </p>
      </div>
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
import CountryField from "@/components/fields/CountryField"
import DoseFilterModal from "./DoseFilterModal"
import DateFilterField from "./DateFilterField"
import { toOptions } from "@/utils/forms.js"
import { setDocumentTitle } from "@/utils/document"

const store = useRootStore()
store.fetchDeclarationFieldsData()

const router = useRouter()
const route = useRoute()
const searchTerm = ref(route.query.recherche)
const activeAccordion = ref()

const opened = ref(false)

// Valeurs obtenus du queryparams

const page = computed(() => parseInt(route.query.page))
const filteredStatus = computed(() => route.query.status)
const ordering = computed(() => route.query.triage)
const article = computed(() => route.query.article)
const population = computed(() => (route.query.population ? parseInt(route.query.population) : ""))
const condition = computed(() => (route.query.condition ? parseInt(route.query.condition) : ""))
const galenicFormulation = computed(() => (route.query.formeGalenique ? parseInt(route.query.formeGalenique) : ""))
const country = computed(() => route.query.pays)
const dose = computed(() => route.query.dose)
const limit = computed(() => route.query.limit)
const submissionDateAfter = computed(() => route.query.soumissionAvant)
const submissionDateBefore = computed(() => route.query.soumissionApres)
const decisionDateAfter = computed(() => route.query.decisionAvant)
const decisionDateBefore = computed(() => route.query.decisionApres)

// Mises à jour de la requête lors des changements des filtres et recherche

const updateQuery = (newQuery) => {
  router.push({ query: { ...route.query, ...{ page: 1 }, ...newQuery } })
}

const updateStatusFilter = (status) => updateQuery({ status })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateOrdering = (newValue) => updateQuery({ triage: newValue })
const updateArticle = (newValue) => updateQuery({ article: newValue })
const updatePopulation = (newValue) => updateQuery({ population: newValue })
const updateCondition = (newValue) => updateQuery({ condition: newValue })
const updateGalenicFormulation = (newValue) => updateQuery({ formeGalenique: newValue })
const updateCountry = (newValue) => updateQuery({ pays: newValue })
const updateDose = (newValue) => updateQuery({ dose: newValue })
const updateLimit = (newValue) => updateQuery({ limit: newValue })
const updateComposition = () =>
  updateQuery({ composition: ingredientsToFilter.value.map((x) => x.join("||")).join("|||") })
const updateSubmissionDateAfter = (newValue) => updateQuery({ soumissionAvant: newValue })
const updateSubmissionDateBefore = (newValue) => updateQuery({ soumissionApres: newValue })
const updateDecisionDateAfter = (newValue) => updateQuery({ decisionAvant: newValue })
const updateDecisionDateBefore = (newValue) => updateQuery({ decisionApres: newValue })

const hasDeclarations = computed(() => data.value?.count > 0)
const showPagination = computed(() => data.value?.count > data.value?.results?.length)
const offset = computed(() => (page.value - 1) * limit.value)

const search = () => updateQuery({ recherche: searchTerm.value })

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

const maxDownloadSize = 5000
const canDownloadFile = computed(() => (data.value?.count || 0) <= maxDownloadSize)

// Requêtes

const apiQueryParams = computed(() => {
  const limitQuery = limit.value ? `?limit=${limit.value}` : "?"
  const offsetQuery = offset.value ? `&offset=${offset.value}` : ""
  const statusQuery = filteredStatus.value ? `&status=${filteredStatus.value}` : ""
  const orderingQuery = ordering.value ? `&ordering=${ordering.value}` : ""
  const articleQuery = article.value ? `&article=${article.value}` : ""
  const populationQuery = population.value ? `&population=${population.value}` : ""
  const conditionQuery = condition.value ? `&condition=${condition.value}` : ""
  const galenicFormulationQuery = galenicFormulation.value ? `&galenic_formulation=${galenicFormulation.value}` : ""
  const countryQuery = country.value ? `&country=${country.value}` : ""
  const doseQuery = dose.value ? `&dose=${dose.value}` : ""
  const submissionDateAfterQuery = submissionDateAfter.value
    ? `&submission_date_after=${submissionDateAfter.value}`
    : ""
  const submissionDateBeforeQuery = submissionDateBefore.value
    ? `&submission_date_before=${submissionDateBefore.value}`
    : ""
  const decisionDateAfterQuery = decisionDateAfter.value ? `&decision_date_after=${decisionDateAfter.value}` : ""
  const decisionDateBeforeQuery = decisionDateBefore.value ? `&decision_date_before=${decisionDateBefore.value}` : ""
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

  const queryParams = `/${limitQuery}${offsetQuery}${statusQuery}${orderingQuery}${articleQuery}${populationQuery}${conditionQuery}${galenicFormulationQuery}${searchQuery}${plantsQuery}${microorganismsQuery}${substancesQuery}${ingredientsQuery}${countryQuery}${doseQuery}${submissionDateAfterQuery}${submissionDateBeforeQuery}${decisionDateAfterQuery}${decisionDateBeforeQuery}`

  // Enlève les `&` consecutifs
  return queryParams.replace(/&+/g, "&").replace(/&$/, "")
})
const apiUrl = computed(() => `/api/v1/declarations${apiQueryParams.value}`)
const excelUrl = computed(() => `/api/v1/declarations-export.xlsx${apiQueryParams.value}`)

const { response, data, isFetching, execute } = useFetch(apiUrl, { headers: { Accept: "application/json" } })
  .get()
  .json()

watch(route, async () => {
  await execute()
  if (response?.value) await handleError(response) // Utile pour éviter des traiter les NS_BINDING_ABORTED de Firefox
  setDocumentTitle(["Recherche avancée"], {
    number: page.value,
    total: pages.value.length,
    term: "page",
  })
})

// Remplissage d'options dans les champs select

const { populations, conditions, galenicFormulations } = storeToRefs(store)

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
@reference "../../styles/index.css";

.search-area :deep(.fr-select-group) {
  @apply my-0!;
}
.filter-area :deep(.fr-fieldset__legend) {
  @apply py-0!;
}
.filter-area :deep(.fr-fieldset__element) {
  @apply my-0!;
}
.status-filter :deep(.fr-fieldset__element) {
  @apply my-2!;
}
div.seeOverflow :deep(#filter-accordeon.fr-collapse--expanded) {
  overflow: visible;
}
</style>
