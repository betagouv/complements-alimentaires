<template>
  <div class="bg-blue-france-925 py-8">
    <!-- Search -->
    <div class="fr-container">
      <DsfrSearchBar
        placeholder="Rechercher par ingrédient, plante, substance..."
        v-model="searchTerm"
        @search="search"
      />
    </div>
  </div>

  <!-- Element -->
  <div class="fr-container">
    <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />
  </div>
  <template v-if="element">
    <div class="fr-container my-8">
      <h1 class="fr-h4 !mb-1 capitalize">{{ element.name }}</h1>

      <div class="flex flex-col flex-nowrap sm:flex-row sm:flex-wrap gap-1 sm:gap-20 mb-8">
        <ElementColumn title="Type">
          <div class="flex gap-x-1">
            <div><v-icon scale="0.75" :name="icon" /></div>
            <ElementText :text="getTypeInFrench(type)" />
          </div>
        </ElementColumn>

        <ElementColumn title="Synonymes" v-if="synonyms?.length">
          <ElementTag :label="synonym" v-for="synonym in synonyms" :key="synonym" />
        </ElementColumn>

        <ElementColumn title="Famille" v-if="family">
          <ElementText :text="family" />
        </ElementColumn>

        <ElementColumn title="Genre" v-if="genre">
          <ElementText :text="genre" />
        </ElementColumn>

        <ElementColumn title="Numéro CAS" v-if="casNumber">
          <ElementText :text="casNumber" />
        </ElementColumn>

        <ElementColumn title="Numéro EINEC" v-if="einecNumber">
          <ElementText :text="einecNumber" />
        </ElementColumn>

        <ElementColumn title="Apport nutritionnel de référence" v-if="nutritionalReference">
          <ElementText :text="nutritionalReference" :lowercase="true" />
        </ElementColumn>

        <ElementColumn title="Quantité maximale autorisée" v-if="maxQuantity">
          <ElementText :text="maxQuantity" :lowercase="true" />
        </ElementColumn>

        <ElementColumn title="Parties utiles" v-if="plantParts?.length">
          <ElementTag :label="part" v-for="part in plantParts" :key="part" />
        </ElementColumn>

        <ElementColumn title="Substances" v-if="substances?.length">
          <ElementTag
            :link="{
              name: 'ElementPage',
              params: { urlComponent: `${substance.id}--substance--${substance.name}` },
            }"
            :label="substance.name"
            v-for="substance in substances"
            :key="`substance-${substance.id}`"
          />
        </ElementColumn>

        <ElementColumn title="Statut" v-if="status">
          <ElementStatusBadge :text="status" />
        </ElementColumn>
      </div>

      <ElementTextSection title="Description" :text="description" />
      <ElementTextSection title="Commentaires" :text="publicComments" />
      <!-- Date de dernière mise à jour de la donnée -->
      <DsfrAccordion
        title="Historique de l'ingrédient"
        id="accordion-history"
        :expanded-id="expandedId"
        @expand="(id) => (expandedId = id)"
      >
        <DsfrTable :rows="historyDataDedup"></DsfrTable>
      </DsfrAccordion>
    </div>

    <!-- Rapporter un problème dans les données -->
    <div class="bg-blue-france-975 py-8">
      <div class="fr-container">
        <ReportIssueBlock :elementName="element.name" />
      </div>
    </div>
  </template>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { getTypeIcon, getTypeInFrench, unSlugify, getApiType } from "@/utils/mappings"
import { useRoute, useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import ElementColumn from "./ElementColumn.vue"
import ElementTag from "./ElementTag.vue"
import ElementStatusBadge from "@/components/ElementStatusBadge.vue"
import ElementText from "./ElementText.vue"
import ElementTextSection from "./ElementTextSection.vue"
import ReportIssueBlock from "./ReportIssueBlock.vue"

const route = useRoute()
const router = useRouter()
const notFound = ref(false)

const searchTerm = ref(null)
const search = () => {
  if (searchTerm.value.length < 3) window.alert("Veuillez saisir au moins trois caractères")
  else router.push({ name: "ElementSearchResultsPage", query: { q: searchTerm.value } })
}

// Afin d'améliorer le SEO, l'urlComponent prend la forme id--type--name
const props = defineProps({ urlComponent: String })
const elementId = computed(() => props.urlComponent.split("--")[0])
const type = computed(() => unSlugify(props.urlComponent.split("--")[1]))
const icon = computed(() => getTypeIcon(type))
// Information affichée
const family = computed(() => element.value?.family?.name)
const genre = computed(() => element.value?.genre)
const plantParts = computed(() =>
  element.value?.plantParts?.filter((x) => x.isUseful === true && !!x.name).map((x) => x.name)
)
const substances = computed(() => element.value?.substances)
const synonyms = computed(() => element.value?.synonyms?.map((x) => x.name).filter((x) => !!x))
const casNumber = computed(() => element.value?.casNumber)
const einecNumber = computed(() => element.value?.einecNumber)
const status = computed(() => element.value?.status)
const nutritionalReference = computed(() => {
  if (element.value?.unit && element.value?.nutritionalReference)
    return element.value?.nutritionalReference + " " + element.value?.unit
  else return null
})
const maxQuantity = computed(() => {
  if (element.value?.unit && element.value?.maxQuantity) return element.value?.maxQuantity + " " + element.value?.unit
  else return null
})
const description = computed(() => element.value?.description)
const publicComments = computed(() => element.value?.publicComments)

const historyData = computed(() =>
  element.value?.history
    .filter((item) => item.historyChangeReason)
    .map((item) => [
      new Date(item.historyDate).toLocaleString("default", { month: "long", year: "numeric" }),
      item.historyChangeReason,
    ])
)
// Deduplication en passant par une string
const historyDataDedup = computed(() => Array.from(new Set(historyData.value.map(JSON.stringify)), JSON.parse))

// TODO: remove background
// TODO: affichage du change reason dans l'admin
const url = computed(() => `/api/v1/${getApiType(type).value}/${elementId.value}`)
const { data: element, response, execute } = useFetch(url, { immediate: false }).get().json()

const getElementFromApi = async () => {
  if (!type.value || !elementId.value) {
    console.log(props.urlComponent.split("--")[1])
    notFound.value = true
    return
  }
  await execute()
  await handleError(response)
}

const searchPageSource = ref(null)
const expandedId = ref(null)

const breadcrumbLinks = computed(() => {
  const links = [{ to: "/", text: "Accueil" }]
  if (searchPageSource.value) links.push({ to: searchPageSource, text: "Résultats de recherche" })
  links.push({ text: element.value?.name || "" })
  return links
})

// Init
if (router.options.history.state.back && router.options.history.state.back.indexOf("resultats") > -1)
  searchPageSource.value = router.options.history.state.back
getElementFromApi()

watch(element, (newElement) => {
  if (newElement) document.title = `${newElement.name} - Compl'Alim`
})

watch(route, getElementFromApi)
</script>
<style scoped>
.fr-table :deep(table) {
  @apply !table;
}
</style>
