<template>
  <div class="bg-blue-france-925 py-8">
    <!-- Search -->
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

  <!-- Element -->
  <div class="fr-container">
    <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />
  </div>
  <template v-if="element">
    <div class="fr-container my-8">
      <h1 class="fr-h4 mb-1! capitalize">
        {{ element.name }}
        <DsfrBadge v-if="novelFood" label="Novel Food" small type="new" />
      </h1>
      <RegulatoryWarning class="mt-4" />

      <div class="flex flex-col flex-nowrap sm:flex-row sm:flex-wrap gap-1 sm:gap-x-20 mb-8">
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

        <ElementColumn title="Parties autorisées" v-if="plantParts?.length">
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

        <ElementColumn title="Activité" v-if="activity">
          <ElementTag :label="activity" />
        </ElementColumn>

        <ElementColumn title="Statut" v-if="status">
          <ElementStatusBadge :text="status" />
        </ElementColumn>

        <ElementColumn title="Apport nutritionnel de référence" v-if="nutritionalReference">
          <ElementText :text="nutritionalReference" :lowercase="true" />
        </ElementColumn>
      </div>
      <ElementTextSection title="Description" :text="description" />

      <ElementDoses
        v-if="element.maxQuantities && element.maxQuantities.length"
        :maxQuantities="element.maxQuantities"
        :unit="element.unit"
      ></ElementDoses>
      <div v-if="element.warningsOnLabel">
        <h2 class="fr-h6 mb-1!">Avertissement à faire figurer sur l'étiquetage</h2>
        <ul>
          <li v-for="(_, idx) in element.warningsOnLabel" :key="`warning-${idx}`">
            {{ element.warningsOnLabel[idx] }}
          </li>
        </ul>
      </div>
      <!-- Utiliser DsfrCallout avec une couleur particulière pour les avertissements quand cela sera possible https://github.com/dnum-mi/vue-dsfr/issues/1126 -->

      <ElementTextSection
        v-if="element.requiresAnalysisReport"
        title="Point d'attention"
        text="Un bulletin d'analyse vous sera demandé."
      />
      <ElementTextSection title="Commentaires" :text="publicComments" />
      <ul v-if="element.regulatoryResourceLinks?.length" class="list-none -ml-4 mb-6">
        <li v-for="resourceLink in element.regulatoryResourceLinks" :key="resourceLink">
          Ressource reglementaire :
          <a :href="`${resourceLink}`" target="_blank" ref="noopener noreferrer">
            {{ resourceLink }}
          </a>
        </li>
      </ul>
      <!-- Date de dernière mise à jour de la donnée -->
      <DsfrAccordion title="Historique de l'ingrédient" id="accordion-history">
        <DsfrTable
          :headers="historyHeaders"
          :rows="historyDataDedup"
          title="Historique de l'ingrédient"
          :no-caption="true"
        ></DsfrTable>
      </DsfrAccordion>

      <div v-if="isInstructor" class="text-right mt-4">
        <p class="mb-2"><em>Vous avez le role d'instruction :</em></p>
        <div class="flex justify-end items-center">
          <router-link
            :to="{ name: 'AdvancedSearchPage', query: { composition: `${element.id}||${element.name}||${type}` } }"
            class="h-fit"
          >
            Voir les déclarations concernées
          </router-link>
          <router-link
            :to="{ name: 'ModifyElement', params: { urlComponent: props.urlComponent } }"
            class="fr-btn fr-btn--tertiary fr-btn--sm ml-4"
          >
            <v-icon name="ri-pencil-line" :scale="0.85" class="mr-1"></v-icon>
            Modifier
          </router-link>
        </div>
      </div>
    </div>

    <!-- Rapporter un problème dans les données -->
    <div class="bg-blue-france-975 py-8">
      <div class="fr-container">
        <ReportIssueBlock :elementType="type" :element="element" />
      </div>
    </div>
  </template>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { getTypeIcon, getTypeInFrench, unSlugifyType, slugifyType, getApiType } from "@/utils/mappings"
import { useRoute, useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { useRootStore } from "@/stores/root"
import ElementColumn from "./ElementColumn.vue"
import ElementTag from "./ElementTag.vue"
import ElementStatusBadge from "@/components/ElementStatusBadge.vue"
import ElementText from "./ElementText.vue"
import ElementTextSection from "./ElementTextSection.vue"
import ElementAutocomplete from "@/components/ElementAutocomplete"
import ReportIssueBlock from "./ReportIssueBlock.vue"
import ElementDoses from "@/components/ElementDoses.vue"
import RegulatoryWarning from "@/components/RegulatoryWarning.vue"
import { setDocumentTitle } from "@/utils/document"

const store = useRootStore()
const route = useRoute()
const router = useRouter()
const notFound = ref(false)

const searchTerm = ref(null)
const search = (newTerm) => {
  if (newTerm.length < 3) window.alert("Veuillez saisir au moins trois caractères")
  else router.push({ name: "ElementSearchResultsPage", query: { q: newTerm } })
}

const goToSelectedOption = (option) => {
  const slugguedType = slugifyType(option.objectType)
  const urlComponent = `${option?.id}--${slugguedType}--${option?.name}`
  return router.push({ name: "ElementPage", params: { urlComponent } })
}

// Afin d'améliorer le SEO, l'urlComponent prend la forme id--type--name
const props = defineProps({ urlComponent: String })
const elementId = computed(() => props.urlComponent.split("--")[0])
const type = computed(() => unSlugifyType(props.urlComponent.split("--")[1]))
const icon = computed(() => getTypeIcon(type.value))
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
const activity = computed(() => (element.value?.activity ? "Actif" : "Non actif"))
const status = computed(() =>
  ["autorisé", "non autorisé"].includes(element.value?.status) ? element.value?.status : null
)
const novelFood = computed(() => element.value?.novelFood)
const nutritionalReference = computed(() => {
  if (element.value?.unit && (element.value?.nutritionalReference || element.value.nutritionalReference == 0))
    return element.value?.nutritionalReference.toLocaleString("fr-FR") + " " + element.value?.unit
  else return null
})

const description = computed(() => element.value?.description)
const warningOnLabel = computed(() => element.value?.warningOnLabel)
const publicComments = computed(() => element.value?.publicComments)

const historyData = computed(() =>
  element.value?.history
    .filter((item) => item.changedFields?.length || item.historyType === "+" || item.historyPublicChangeReason)
    .map((item) => [
      new Date(item.historyDate).toLocaleString("default", { day: "numeric", month: "short", year: "numeric" }),
      item.historyType === "+" ? "Création de l'ingrédient" : item.changedFields.map((f) => `« ${f} »`).join(", "),
      item.historyPublicChangeReason,
    ])
)

// Deduplication en passant par une string
const historyDataDedup = computed(() => Array.from(new Set(historyData.value.map(JSON.stringify)), JSON.parse))

const historyHeaders = ["Date de changement", "Champs modifiés", "Détail"]

// TODO: remove background
const url = computed(() => `/api/v1/${getApiType(type.value)}s/${elementId.value}?history=true`)
const { data: element, response, execute } = useFetch(url, { immediate: false }).get().json()

const getElementFromApi = async () => {
  if (!type.value || !elementId.value) {
    notFound.value = true
    return
  }
  await execute()
  await handleError(response)
}

const searchPageSource = ref(null)

const breadcrumbLinks = computed(() => {
  const links = [{ to: { name: "ProducerHomePage" }, text: "Recherche ingrédients" }]
  if (searchPageSource.value) links.push({ to: searchPageSource, text: "Résultats de recherche" })
  links.push({ text: element.value?.name || "" })
  return links
})

// Init
if (router.options.history.state.back && router.options.history.state.back.indexOf("resultats") > -1)
  searchPageSource.value = router.options.history.state.back
getElementFromApi()

watch(element, (newElement) => {
  if (newElement) setDocumentTitle([newElement.name])
})

watch(route, getElementFromApi)

const isInstructor = computed(() => store.loggedUser?.globalRoles?.some((x) => x.name === "InstructionRole"))
</script>

<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
.fr-container :deep(input),
.fr-container :deep(button) {
  @apply mt-0!;
}
</style>
