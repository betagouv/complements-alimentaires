<template>
  <div>
    <!-- Zone de recherche -->
    <div>
      <DsfrFieldset class="mb-0! max-w-2xl">
        <ElementAutocomplete
          v-model="searchTerm"
          label="Rechercher par produit, marque, entreprise ou ingrédient"
          label-visible
          class="max-w-2xl"
          @selected="addIngredient"
          :hideSearchButton="true"
          :chooseFirstAsDefault="false"
          :searchAll="true"
          :extendedSearch="true"
          @searchProduct="searchByProduct"
          @searchBrand="searchByBrand"
          @searchCompany="searchByCompany"
          :required="false"
        />
      </DsfrFieldset>
    </div>
    <!-- Zone des filtres actifs -->
    <div class="mb-4">
      <DsfrTag
        v-for="(item, idx) in activeFilters"
        :key="`active-filters-${idx}`"
        :label="item.text"
        tagName="button"
        @click="item.callback"
        :aria-label="`Retirer le filtre « ${item.text} »`"
        class="mx-1 fr-tag--dismiss"
      ></DsfrTag>
    </div>

    <DsfrAccordionsGroup v-model="activeAccordion">
      <DsfrAccordion title="Filtrer les déclarations">
        <div class="grid grid-cols-4 gap-0 sm:gap-2 md:gap-4">
          <div class="col-span-4 sm:col-span-2 md:col-span-1">
            <DsfrToggleSwitch
              label="Afficher les déclarations à surveiller uniquement"
              :modelValue="surveillanceOnly"
              @update:modelValue="updateSurveillanceOnly"
            />
          </div>
          <div class="col-span-4 sm:col-span-2 md:col-span-1">
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
          </div>
          <div class="col-span-4 sm:col-span-2 md:col-span-1">
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
          </div>
          <div class="col-span-4 sm:col-span-2 md:col-span-1">
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
          </div>
        </div>
      </DsfrAccordion>
    </DsfrAccordionsGroup>

    <hr class="mt-6 mb-0" />

    <IngredientFilterAccordeon v-for="dose in doses" :key="dose" :modelValue="dose" @remove="removeIngredient" />

    <div v-if="isFetching && !data" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else>
      <ControlDeclarationsTable :data="data" v-if="data" @sort="updateOrdering" @filter="updateFiltering" />
      <DsfrPagination
        v-if="showPagination"
        @update:currentPage="updatePage"
        :pages="pages"
        :current-page="page - 1"
        :truncLimit="5"
      />
    </div>
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { computed, watch } from "vue"
import { getPagesForPagination } from "@/utils/components"
import { useRoute, useRouter } from "vue-router"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import ControlDeclarationsTable from "./ControlDeclarationsTable"
import { ref } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { toOptions } from "@/utils/forms.js"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import { typesMapping } from "@/utils/mappings"
import IngredientFilterAccordeon from "./IngredientFilterAccordeon"

const store = useRootStore()
store.fetchDeclarationFieldsData()
const { populations, conditions, galenicFormulations } = storeToRefs(store)

const activeAccordion = ref()

const props = defineProps({ companyId: String })

const router = useRouter()
const route = useRoute()

const offset = computed(() => (page.value - 1) * limit.value)
const pages = computed(() => getPagesForPagination(data.value?.count, limit.value, route.path))

const searchTerm = ref(route.query.recherche || "")

const page = computed(() => parseInt(route.query.page))
const ordering = computed(() => route.query.triage)
const limit = computed(() => parseInt(route.query.limit))
const simplifiedStatus = computed(() => route.query.simplifiedStatus)
const surveillanceOnly = computed(() => route.query.surveillanceOnly === "true")

const population = computed(() => (route.query.population ? parseInt(route.query.population) : ""))
const condition = computed(() => (route.query.condition ? parseInt(route.query.condition) : ""))
const galenicFormulation = computed(() => (route.query.formeGalenique ? parseInt(route.query.formeGalenique) : ""))

const searchTermProduct = computed(() => route.query.rechercheProduit || "")
const searchTermBrand = computed(() => route.query.rechercheMarque || "")
const searchTermCompany = computed(() => route.query.rechercheEntreprise || "")

const showPagination = computed(() => data.value?.count > data.value?.results?.length)

const doses = computed(() => (route.query.doses ? JSON.parse(decodeURIComponent(route.query.doses)) : []))

// Obtention de la donnée via API
const url = computed(() => {
  let apiUrl = `/api/v1/control/declarations/?limit=${limit.value}&offset=${offset.value}&ordering=${ordering.value}&simplifiedStatus=${simplifiedStatus.value}&surveillanceOnly=${surveillanceOnly.value}&search=${searchTerm.value}&`
  if (props.companyId) apiUrl += `${apiUrl}&company=${props.companyId}`
  if (population.value) apiUrl += `&population=${population.value}`
  if (condition.value) apiUrl += `&condition=${condition.value}`
  if (galenicFormulation.value) apiUrl += `&galenic_formulation=${galenicFormulation.value}`
  if (searchTermProduct.value) apiUrl += `&search_name=${searchTermProduct.value}`
  if (searchTermBrand.value) apiUrl += `&search_brand=${searchTermBrand.value}`
  if (searchTermCompany.value) apiUrl += `&search_company=${searchTermCompany.value}`
  if (doses.value) for (let i = 0; i < doses.value.length; i++) apiUrl += `&dose=${doses.value[i]}`

  return apiUrl
})
const { response, data, isFetching, execute } = useFetch(url).get().json()

const fetchSearchResults = async () => {
  await execute()
  await handleError(response)
}

// Mise à jour des paramètres
const updateQuery = (newQuery) => router.push({ query: { ...route.query, ...{ page: 1 }, ...newQuery } })
const updateSurveillanceOnly = (value) => updateQuery({ surveillanceOnly: value ? "true" : "false" })
const updatePage = (newPage) => updateQuery({ page: newPage + 1 })
const updateOrdering = (sortValue) => updateQuery({ triage: sortValue || "-creationDate" })
const updateFiltering = (filterKey, filterValue) => {
  const filterQuery = {}
  filterQuery[filterKey] = filterValue
  updateQuery(filterQuery)
}
const updatePopulation = (newValue) => updateQuery({ population: newValue })
const updateCondition = (newValue) => updateQuery({ condition: newValue })
const updateGalenicFormulation = (newValue) => updateQuery({ formeGalenique: newValue })

const searchByProduct = (term) => updateQuery({ rechercheProduit: term }) && clearSearch()
const searchByBrand = (term) => updateQuery({ rechercheMarque: term }) && clearSearch()
const searchByCompany = (term) => updateQuery({ rechercheEntreprise: term }) && clearSearch()

const updateDoses = (newValue) => updateQuery({ doses: encodeURIComponent(JSON.stringify(newValue)) })

const clearSearch = () => (searchTerm.value = "")

watch(
  [
    page,
    limit,
    ordering,
    simplifiedStatus,
    surveillanceOnly,
    population,
    condition,
    galenicFormulation,
    searchTermProduct,
    searchTermBrand,
    searchTermCompany,
    doses,
  ],
  fetchSearchResults
)

// Filter options

const populationOptions = computed(() => toOptions(populations.value))
const conditionOptions = computed(() => toOptions(conditions.value))
const galenicFormulationOptions = computed(() => toOptions(galenicFormulations.value))

// Filter tags

const activeFilters = computed(() => {
  const filters = []
  if (surveillanceOnly.value)
    filters.push({
      text: "Déclarations à surveiller",
      callback: () => updateSurveillanceOnly(false),
    })
  if (population.value)
    filters.push({
      text: `Pop. cible : ${populationOptions.value?.find((x) => x.value === population.value)?.text || ""}`,
      callback: () => updatePopulation(""),
    })
  if (condition.value)
    filters.push({
      text: `Pop. à risque : ${conditionOptions.value?.find((x) => x.value === condition.value)?.text || ""}`,
      callback: () => updateCondition(""),
    })
  if (galenicFormulation.value)
    filters.push({
      text: `Forme : ${galenicFormulationOptions.value?.find((x) => x.value === galenicFormulation.value)?.text || ""}`,
      callback: () => updateGalenicFormulation(""),
    })
  if (searchTermProduct.value)
    filters.push({
      text: `Produit contenant « ${searchTermProduct.value} »`,
      callback: () => searchByProduct(""),
    })
  if (searchTermBrand.value)
    filters.push({
      text: `Marque contenant « ${searchTermBrand.value} »`,
      callback: () => searchByBrand(""),
    })
  if (searchTermCompany.value)
    filters.push({
      text: `Enterprise contenant « ${searchTermCompany.value} »`,
      callback: () => searchByCompany(""),
    })
  if (doses.value.length > 0) {
    for (let i = 0; i < doses.value.length; i++) {
      const dose = doses.value[i]
      const parts = dose.split("||")
      const type = typesMapping[parts[0]] || "Ingrédient"
      const name = parts[1] || "Inconnu"
      const doseText = `${type} : ${name}`
      filters.push({
        text: doseText,
        callback: () => removeIngredient(dose),
      })
    }
  }
  return filters
})

const addIngredient = async (ingredient) => {
  // Temporairement on traite les ajouts d'ingrédients comme ayant une dose supérieure à 0
  // Par la suite on pourra spécifier également la dose précise recherchée et la partie de
  // plante
  let newFilterString = `${ingredient.objectType}||${ingredient.name}||${ingredient.id}`

  if (ingredient.objectType === "plant") newFilterString += "|-|Toutes les parties"

  newFilterString += "||>||0||"

  clearSearch()
  updateDoses([...doses.value, newFilterString])
}
const removeIngredient = (ingredient) => {
  const newDoses = doses.value.filter((x) => x !== ingredient)
  updateDoses(newDoses)
}
</script>

<style scoped>
@reference "../../../styles/index.css";
div :deep(.fr-select-group) {
  @apply mb-0;
  @apply sm:mb-2;
}
</style>
