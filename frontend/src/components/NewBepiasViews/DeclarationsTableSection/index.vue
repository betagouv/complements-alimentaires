<template>
  <div>
    <!-- Zone de recherche -->
    <div>
      <DsfrFieldset class="mb-0! max-w-2xl">
        <!-- <DsfrSearchBar
          v-model="searchTerm"
          label="Rechercher par produit, marque, entreprise ou ingrédient"
          placeholder="Rechercher par produit, marque, entreprise ou ingrédient"
          @search="search"
          @update:modelValue="(val) => val === '' && search()"
        /> -->
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
          @searchProduct="(v) => console.log(`Product : ${v}`)"
          @searchBrand="(v) => console.log(`Brand : ${v}`)"
          @searchCompany="(v) => console.log(`Company : ${v}`)"
          :required="false"
        />
      </DsfrFieldset>
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

    <!-- Zone des filtres actifs -->
    <div class="my-4">
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

const showPagination = computed(() => data.value?.count > data.value?.results?.length)

// Obtention de la donnée via API
const url = computed(() => {
  let apiUrl = `/api/v1/control/declarations/?limit=${limit.value}&offset=${offset.value}&ordering=${ordering.value}&simplifiedStatus=${simplifiedStatus.value}&surveillanceOnly=${surveillanceOnly.value}&search=${searchTerm.value}&`
  if (props.companyId) apiUrl += `${apiUrl}&company=${props.companyId}`
  if (population.value) apiUrl += `&population=${population.value}`
  if (condition.value) apiUrl += `&condition=${condition.value}`
  if (galenicFormulation.value) apiUrl += `&galenic_formulation=${galenicFormulation.value}`
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

watch(
  [page, limit, ordering, simplifiedStatus, surveillanceOnly, population, condition, galenicFormulation],
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
  return filters
})

// Search

const addIngredient = async (ingredient) => {
  // selectedIngredient.value = ingredient
  // if (!ingredientIsPlant.value) selectedPart.value = null
  // if (ingredientIsSubstance.value) selectedUnit.value = selectedIngredient.value.unit
  // if (
  //   selectedIngredient.value?.objectType === "form_of_supply" ||
  //   selectedIngredient.value?.objectType === "active_ingredient"
  // ) {
  //   const url = `/api/v1/${getApiType(selectedIngredient.value?.objectType)}s/${selectedIngredient.value.id}`
  //   const { data } = await useFetch(url, { immediate: true }).get().json()
  //   selectedIngredient.value.substances = data.value?.substances
  // }
  console.log(ingredient)
}
</script>

<style scoped>
@reference "../../../styles/index.css";
div :deep(.fr-select-group) {
  @apply mb-0;
  @apply sm:mb-2;
}
</style>
