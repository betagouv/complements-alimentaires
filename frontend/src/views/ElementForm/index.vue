<template>
  <div class="mb-8">
    <div class="bg-blue-france-950 py-1">
      <div class="fr-container">
        <DsfrBreadcrumb :links="breadcrumbLinks" />

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

      <FormFields :element="element" :type="apiType" />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { getTypeIcon, getTypeInFrench, unSlugifyType, getApiType } from "@/utils/mappings"
import { useRoute, useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import FormFields from "./FormFields"

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
const router = useRouter()

const url = computed(() => `/api/v1/${apiType.value}s/${elementId.value}?history=true`)
const { data: element, response, execute } = useFetch(url, { immediate: false }).get().json()

const getElementFromApi = async () => {
  if (!type.value || !elementId.value) return // create new ingredient
  await execute()
  await handleError(response)
}
getElementFromApi()

const pageTitle = computed(() => (isNewIngredient.value ? "Nouvel ingrédient" : "Modification ingrédient"))

const breadcrumbLinks = computed(() => {
  const lastRoute = router.getPreviousRoute().value
  const links = []
  if (lastRoute?.name == "ElementPage") {
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

const forms = {
  plant: "Plante",
  substance: "Substance",
  microorganism: "Micro-organisme",
  ingredient: "Autre ingrédient",
}
</script>
