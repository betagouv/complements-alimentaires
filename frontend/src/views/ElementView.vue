<template>
  <div class="bg-blue-france-925 py-8">
    <div class="fr-container">
      <DsfrSearchBar :placeholder="currentSearch" v-model="searchTerm" @search="search" />
    </div>
  </div>
  <div class="fr-container">
    <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />
  </div>
  <div v-if="element" class="fr-container my-8">
    <h1 class="fr-h4 !mb-1 capitalize">{{ element.name }}</h1>

    <div class="flex flex-col flex-nowrap sm:flex-row sm:flex-wrap gap-1 sm:gap-20 mb-8">
      <div class="col-span-12 sm:col-span-4 md:col-span-3 flex flex-col mt-4">
        <div class="fr-text--sm !font-medium !mb-1">Type</div>
        <div class="flex">
          <div><v-icon scale="0.75" class="mr-1" :name="icon" /></div>
          <div class="fr-text--sm !mb-0 capitalize">{{ type === "ingredient" ? "ingrédient" : type }}</div>
        </div>
      </div>

      <div v-if="synonyms && synonyms.length" class="col-span-12 sm:col-span-4 md:col-span-3 flex flex-col mt-4">
        <div class="fr-text--sm !font-medium !mb-1">Synonymes</div>
        <DsfrTag small :label="synonym" v-for="synonym in synonyms" :key="synonym" class="mb-1 capitalize"></DsfrTag>
      </div>

      <div v-if="family" class="col-span-12 sm:col-span-4 md:col-span-3 flex flex-col mt-4">
        <div class="fr-text--sm !font-medium !mb-1">Famille</div>
        <div class="fr-text--sm !mb-0 capitalize">{{ family }}</div>
      </div>

      <div v-if="genre" class="col-span-12 sm:col-span-4 md:col-span-3 flex flex-col mt-4">
        <div class="fr-text--sm !font-medium !mb-1">Genre</div>
        <div class="fr-text--sm !mb-0 capitalize">{{ genre }}</div>
      </div>

      <div v-if="casNumber" class="col-span-12 sm:col-span-4 md:col-span-3 flex flex-col mt-4">
        <div class="fr-text--sm !font-medium !mb-1">Numéro CAS</div>
        <div class="fr-text--sm !mb-0 capitalize">{{ casNumber }}</div>
      </div>

      <div v-if="einecNumber" class="col-span-12 sm:col-span-4 md:col-span-3 flex flex-col mt-4">
        <div class="fr-text--sm !font-medium !mb-1">Numéro EINEC</div>
        <div class="fr-text--sm !mb-0 capitalize">{{ einecNumber }}</div>
      </div>

      <div v-if="usefulParts && usefulParts.length" class="col-span-12 sm:col-span-4 md:col-span-3 flex flex-col mt-4">
        <div class="fr-text--sm !font-medium !mb-1">Parties utiles</div>
        <DsfrTag small :label="part" v-for="part in usefulParts" :key="part" class="mb-1 capitalize"></DsfrTag>
      </div>

      <div v-if="substances && substances.length" class="col-span-12 sm:col-span-4 md:col-span-3 flex flex-col mt-4">
        <div class="fr-text--sm !font-medium !mb-1">Substances</div>
        <DsfrTag
          :link="{ name: 'ElementView', params: { urlComponent: `${substance.id}--substance--${substance.name}` } }"
          small
          :label="substance.name"
          v-for="substance in substances"
          :key="`substance-${substance.id}`"
          class="mb-1 capitalize"
        ></DsfrTag>
      </div>
    </div>

    <h2 class="fr-h6 !mb-1" v-if="description">Description</h2>
    <p>{{ description }}</p>

    <h2 class="fr-h6 !mb-1" v-if="publicComments">Commentaires</h2>
    <p>{{ publicComments }}</p>
  </div>
  <DsfrErrorPage v-else-if="notFound" class="my-8" title="Article non trouvé" />
</template>

<script setup>
import { onMounted, ref, computed, watch } from "vue"
import { verifyResponse, NotFoundError, getTypeIcon } from "@/utils"
import { useRoute, useRouter } from "vue-router"

const searchTerm = ref(null)
const search = () => {
  if (searchTerm.value.length < 3) {
    window.alert("Veuillez saisir au moins trois caractères")
    return
  }
  router.push({ name: "SearchResults", query: { q: searchTerm.value } })
}

const route = useRoute()
const router = useRouter()

const notFound = ref(false)
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
const element = ref(null)

// Information affichée

const family = computed(() => element.value?.family?.name)
const genre = computed(() => element.value?.genre)
const usefulParts = computed(() => element.value?.usefulParts?.map((x) => x.name).filter((x) => !!x))
const substances = computed(() => element.value?.substances)
const synonyms = computed(() => element.value?.synonyms?.map((x) => x.name).filter((x) => !!x))
const casNumber = computed(() => element.value?.casNumber)
const einecNumber = computed(() => element.value?.einecNumber)
const description = computed(() => element.value?.description)
const publicComments = computed(() => element.value?.publicComments)

const getElementFromApi = () => {
  if (!type.value || !elementId.value) {
    notFound.value = true
    return
  }
  return fetch(`/api/v1/${typeMapping[type.value]}s/${elementId.value}`)
    .then(verifyResponse)
    .then((response) => (element.value = response))
    .catch((error) => {
      if (error instanceof NotFoundError) notFound.value = true
      else window.alert("Une erreur est survenue veuillez réessayer plus tard")
    })
}

const searchPageSource = ref(null)

const breadcrumbLinks = computed(() => {
  const links = [{ to: "/", text: "Accueil" }]
  if (searchPageSource.value) links.push({ to: searchPageSource, text: "Résultats de recherche" })
  links.push({ text: element.value?.name || "" })
  return links
})

onMounted(() => {
  if (router.options.history.state.back && router.options.history.state.back.indexOf("resultats") > -1)
    searchPageSource.value = router.options.history.state.back
  getElementFromApi()
})

watch(element, (newElement) => {
  if (newElement) document.title = `${newElement.name} - Compléments alimentaires`
})

watch(route, getElementFromApi)
</script>
