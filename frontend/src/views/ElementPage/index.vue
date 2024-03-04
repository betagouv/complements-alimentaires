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
            <ElementText :text="type === 'ingredient' ? 'ingrédient' : type" />
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

        <ElementColumn title="Parties utiles" v-if="plantParts?.length">
          <ElementTag :label="part" v-for="part in plantParts" :key="part" />
        </ElementColumn>

        <ElementColumn title="Parties à surveiller" v-if="toWatchParts?.length">
          <ElementTag
            :label="part"
            v-for="part in toWatchParts"
            :key="part"
            class="!bg-warning-925 !text-warning-425"
          />
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
      </div>

      <ElementTextSection title="Description" :text="description" />
      <ElementTextSection title="Commentaires" :text="publicComments" />
    </div>

    <!-- Report Issue -->
    <div class="bg-blue-france-975 py-8">
      <div class="fr-container">
        <ReportIssueBlock :elementName="element.name" />
      </div>
    </div>
  </template>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { getTypeIcon } from "@/utils/mappings"
import { useRoute, useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import useToaster from "@/composables/use-toaster"
import ElementColumn from "./ElementColumn.vue"
import ElementTag from "./ElementTag.vue"
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

const typeMapping = {
  plante: "plant",
  "micro-organisme": "microorganism",
  ingredient: "ingredient",
  substance: "substance",
}

// Afin d'améliorer le SEO, l'urlComponent prend la forme id--type--name
const props = defineProps({ urlComponent: String })
const elementId = computed(() => props.urlComponent.split("--")[0])
const type = computed(() => props.urlComponent.split("--")[1])

const icon = computed(() => getTypeIcon(typeMapping[type.value]))

// Information affichée
const family = computed(() => element.value?.family?.name)
const genre = computed(() => element.value?.genre)
const plantParts = computed(() => element.value?.plantParts?.map((x) => x.name).filter((x) => !!x))
const toWatchParts = computed(() =>
  element.value?.plantParts?.filter((x) => x.mustBeMonitored === true && !!x.name).map((x) => x.name)
)
const substances = computed(() => element.value?.substances)
const synonyms = computed(() => element.value?.synonyms?.map((x) => x.name).filter((x) => !!x))
const casNumber = computed(() => element.value?.casNumber)
const einecNumber = computed(() => element.value?.einecNumber)
const description = computed(() => element.value?.description)
const publicComments = computed(() => element.value?.publicComments)

const url = computed(() => `/api/v1/${typeMapping[type.value]}s/${elementId.value}`)
const { data: element, error, execute } = useFetch(url, { immediate: false }).get().json()

const getElementFromApi = async () => {
  if (!type.value || !elementId.value) {
    notFound.value = true
    return
  }
  await execute()
  if (error.value) useToaster().addUnknownErrorMessage()
}

const searchPageSource = ref(null)

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
  if (newElement) document.title = `${newElement.name} - Compléments alimentaires`
})

watch(route, getElementFromApi)
</script>
