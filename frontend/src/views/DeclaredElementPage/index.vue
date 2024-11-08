<template>
  <div>
    <!-- bandeau construction -->
    <DsfrNotice title="Page en construction" />
    <!-- bandeau nouvel ingredient -->
    <!-- breadcrumbs -->
    <div class="fr-container">
      <h1>Nouvel ingrédient</h1>
      <div class="flex">
        <div class="bg-grey-975">
          <p>Plante</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// import { ref, computed, watch } from "vue"
// import { getTypeIcon, getTypeInFrench, unSlugifyType, getApiType } from "@/utils/mappings"
// import { useRoute, useRouter } from "vue-router"
// import { useFetch } from "@vueuse/core"
// import { handleError } from "@/utils/error-handling"

// const route = useRoute()
// const router = useRouter()
// const notFound = ref(false)

// const searchTerm = ref(null)
// const search = () => {
//   if (searchTerm.value.length < 3) window.alert("Veuillez saisir au moins trois caractères")
//   else router.push({ name: "ElementSearchResultsPage", query: { q: searchTerm.value } })
// }

// // Afin d'améliorer le SEO, l'urlComponent prend la forme id--type--name
// const props = defineProps({ urlComponent: String })
// const elementId = computed(() => props.urlComponent.split("--")[0])
// const type = computed(() => unSlugifyType(props.urlComponent.split("--")[1]))
// const icon = computed(() => getTypeIcon(type.value))
// // Information affichée
// const family = computed(() => element.value?.family?.name)
// const genre = computed(() => element.value?.genre)
// const plantParts = computed(() =>
//   element.value?.plantParts?.filter((x) => x.isUseful === true && !!x.name).map((x) => x.name)
// )
// const substances = computed(() => element.value?.substances)
// const synonyms = computed(() => element.value?.synonyms?.map((x) => x.name).filter((x) => !!x))
// const casNumber = computed(() => element.value?.casNumber)
// const einecNumber = computed(() => element.value?.einecNumber)
// const activity = computed(() => (element.value?.activity ? "Actif" : "Non actif"))
// const status = computed(() =>
//   ["autorisé", "non autorisé"].includes(element.value?.status) ? element.value?.status : null
// )
// const nutritionalReference = computed(() => {
//   if (element.value?.unit && (element.value?.nutritionalReference || element.value.nutritionalReference == 0))
//     return element.value?.nutritionalReference + " " + element.value?.unit
//   else return null
// })
// const maxQuantity = computed(() => {
//   if (element.value?.unit && (element.value?.maxQuantity || element.value.maxQuantity == 0))
//     return element.value?.maxQuantity + " " + element.value?.unit
//   else return null
// })
// const description = computed(() => element.value?.description)
// const publicComments = computed(() => element.value?.publicComments)

// const historyData = computed(() =>
//   element.value?.history
//     .filter((item) => item.historyChangeReason)
//     .map((item) => [
//       new Date(item.historyDate).toLocaleString("default", { month: "long", year: "numeric" }),
//       item.historyChangeReason,
//     ])
// )
// // Deduplication en passant par une string
// const historyDataDedup = computed(() => Array.from(new Set(historyData.value.map(JSON.stringify)), JSON.parse))

// // TODO: remove background
// // TODO: affichage du change reason dans l'admin
// const url = computed(() => `/api/v1/${getApiType(type.value)}s/${elementId.value}?history=true`)
// const { data: element, response, execute } = useFetch(url, { immediate: false }).get().json()

// const getElementFromApi = async () => {
//   if (!type.value || !elementId.value) {
//     notFound.value = true
//     return
//   }
//   await execute()
//   await handleError(response)
// }

// const searchPageSource = ref(null)

// const breadcrumbLinks = computed(() => {
//   const links = [{ to: "/", text: "Accueil" }]
//   if (searchPageSource.value) links.push({ to: searchPageSource, text: "Résultats de recherche" })
//   links.push({ text: element.value?.name || "" })
//   return links
// })

// // Init
// if (router.options.history.state.back && router.options.history.state.back.indexOf("resultats") > -1)
//   searchPageSource.value = router.options.history.state.back
// getElementFromApi()

// watch(element, (newElement) => {
//   if (newElement) document.title = `${newElement.name} - Compl'Alim`
// })

// watch(route, getElementFromApi)
</script>
