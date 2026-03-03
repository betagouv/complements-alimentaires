<template>
  <div class="mb-8">
    <div class="bg-blue-france-950 py-1">
      <div class="fr-container">
        <CaBreadcrumb :links="breadcrumbLinks" />

        <h1 class="-mt-6 mb-4">{{ pageTitle }}</h1>
      </div>
    </div>
    <div v-if="isNewIngredient && !type" class="fr-container">
      <div class="grid sm:grid-cols-2 gap-8 sm:p-8 m-8">
        <DsfrTile v-for="(title, type) in forms" :key="type" :title="title" :to="{ query: { type: type } }" />
      </div>
    </div>
    <div v-else class="fr-container">
      <p class="mt-6">
        <v-icon :name="icon" />
        {{ typeName }}
      </p>

      <DsfrTabs v-model="activeTab" :tab-list-name="tabListName" :tab-titles="tabTitles">
        <DsfrTabContent panel-id="form-content" tab-id="form">
          <FormFields :element="element" :type="type" :urlComponent="props.urlComponent" />
        </DsfrTabContent>

        <DsfrTabContent panel-id="history-content" tab-id="history">
          <div class="-my-4 mb-4">
            <DsfrTable
              :headers="headers"
              :rows="historyDataDedup"
              title="Historique de l'ingrédient"
              :no-caption="true"
            />
          </div>
        </DsfrTabContent>
      </DsfrTabs>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import { getTypeIcon, getTypeInFrench, unSlugifyType, getApiType } from "@/utils/mappings"
import { useRoute } from "vue-router"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import FormFields from "./FormFields"
import CaBreadcrumb from "@/components/CaBreadcrumb"
import { setDocumentTitle } from "@/utils/document"

const props = defineProps({ urlComponent: String })

const isNewIngredient = computed(() => !props.urlComponent)

const elementId = computed(() => props.urlComponent?.split("--")[0])
const route = useRoute()
const type = computed(() =>
  isNewIngredient.value ? route.query.type : unSlugifyType(props.urlComponent.split("--")[1])
)
const apiType = computed(() => type.value && getApiType(type.value))
const icon = computed(() => getTypeIcon(type.value))
const typeName = computed(() => getTypeInFrench(type.value))

const url = computed(() => `/api/v1/${apiType.value}s/${elementId.value}?history=true`)
const { data: element, response, execute } = useFetch(url, { immediate: false }).get().json()

const pageTitle = computed(() => (isNewIngredient.value ? "Nouvel ingrédient" : "Modification ingrédient"))

const getElementFromApi = async () => {
  const titleParts = [pageTitle.value]
  if (!type.value || !elementId.value) {
    setDocumentTitle(titleParts)
    return // create new ingredient
  }
  await execute()
  await handleError(response)
  if (element.value?.name) titleParts.push(element.value.name)
  setDocumentTitle(titleParts)
}
getElementFromApi()

const breadcrumbLinks = computed(() => {
  const links = []
  if (props.urlComponent) {
    links.push({ to: { name: "ProducerHomePage" }, text: "Recherche ingrédients" })
    // ce n'est pas possible d'accèder l'URL -2 pour "Résultats de recherche" en utilisant history ou router
    links.push({ to: { name: "ElementPage", params: { urlComponent: props.urlComponent } }, text: element.value?.name })
  } else {
    links.push({ to: { name: "DashboardPage" }, text: "Tableau de bord" })
    links.push({ to: { name: "NewElementsPage" }, text: "Ingrédients pour ajout" })
  }
  links.push({ text: pageTitle })
  return links
})

const activeTab = ref(0)
const tabListName = "Liste d’onglet"
const title1 = "Fiche ingrédient"
const tabTitles = computed(() => {
  const tabs = [{ title: title1, tabId: "form", panelId: "form-content" }]
  if (!isNewIngredient.value) tabs.push({ title: "Historique", tabId: "history", panelId: "history-content" })
  return tabs
})

const forms = {
  plant: "Plante",
  substance: "Substance",
  microorganism: "Micro-organisme",
  ingredient: "Autre ingrédient",
}

const headers = ["Date", "Réalisée par", "Champs modifiés", "Détail (privé)", "Détail (public)"]

const historyData = computed(() =>
  element.value?.history
    .filter(
      (item) =>
        item.changedFields?.length ||
        item.historyType === "+" ||
        item.historyChangeReason ||
        item.historyPublicChangeReason
    )
    .map((item) => [
      new Date(item.historyDate).toLocaleString("default", { day: "numeric", month: "numeric", year: "numeric" }),
      item.user ? `${item.user.firstName} ${item.user.lastName}` : "",
      item.historyType === "+" ? "Création de l'ingrédient" : item.changedFields.map((f) => `« ${f} »`).join(", "),
      item.historyChangeReason,
      item.historyPublicChangeReason,
    ])
)
// Deduplication en passant par une string
const historyDataDedup = computed(() => Array.from(new Set(historyData.value?.map(JSON.stringify)), JSON.parse))
</script>
