<template>
  <h2 class="fr-h6">
    <v-icon class="mr-1" name="ri-flask-line" />
    Ingrédients
  </h2>

  <ElementAutocomplete
    v-model="searchTerm"
    :options="autocompleteResults"
    autocomplete="nothing"
    label="Cherchez un ingrédient"
    label-visible
    class="max-w-md"
    hint="Tapez au moins trois caractères pour démarrer la recherche"
    @selected="selectOption"
  />

  <TransitionGroup mode="out-in" name="list" tag="div" class="mt-4 relative">
    <ElementCard
      @remove="removeElement"
      :element="element"
      v-for="element in chosenElements"
      :key="`element-${element.id}`"
      class="mb-2"
    />
  </TransitionGroup>
  <div v-if="chosenElements.length === 0" class="my-12">
    <v-icon name="ri-information-line" class="mr-1"></v-icon>
    Vous n'avez pas encore saisi d'ingrédients pour votre complément alimentaire
  </div>

  <div v-if="substances?.length">
    <h3 class="fr-h6 !mb-4 !mt-6">Substances</h3>
    <SubstancesTable :substances="substances" />
  </div>
</template>

<script setup>
import { ref, watch, computed } from "vue"
import { useFetch, useDebounceFn } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import ElementCard from "./ElementCard.vue"
import SubstancesTable from "./SubstancesTable.vue"
import useToaster from "@/composables/use-toaster"

const autocompleteResults = ref([])
const searchTerm = ref("")
const chosenElements = ref([])
const debounceDelay = 350

const substances = computed(() => {
  const substances = chosenElements.value
    .map((x) => (x.objectType === "substance" ? [x] : x.substances))
    .flat()
    .filter((x) => !!x)
  // Remove duplicates
  return substances.filter((x, idx) => substances.findIndex((y) => y.id === x.id) === idx)
})

const elementIndex = (element) =>
  chosenElements.value.findIndex((x) => x.id === element.id && x.objectType === element.objectType)

const selectOption = async (result) => {
  const isDuplicate = elementIndex(result) > -1
  autocompleteResults.value = []
  searchTerm.value = ""
  if (isDuplicate) return
  const element = await fetchElement(result.objectType, result.id)
  chosenElements.value.unshift(element)
}

const removeElement = (element) => chosenElements.value.splice(elementIndex(element), 1)

const fetchAutocompleteResults = useDebounceFn(async () => {
  if (searchTerm.value.length < 3) {
    autocompleteResults.value = []
    return
  }

  const body = { term: searchTerm.value }
  const { error, data } = await useFetch("/api/v1/elements/autocomplete/", { headers }).post(body).json()

  if (error.value) {
    useToaster().addMessage({
      type: "error",
      title: "Erreur",
      description: "Une erreur avec la recherche est survenue, veuillez réessayer plus tard.",
      id: "autocomplete-error",
    })
    return
  }
  autocompleteResults.value = data.value
}, debounceDelay)

const fetchElement = async (type, id) => {
  const { error, data } = await useFetch(`/api/v1/${type}s/${id}`).get().json()
  if (error.value) {
    useToaster().addErrorMessage("Une erreur est survenue en ajoutant cet élément, veuillez réessayer plus tard.")
    return null
  }
  return { ...data.value, ...{ objectType: type } }
}

watch(searchTerm, fetchAutocompleteResults)
</script>

<style scoped>
.list-move,
.list-enter-active {
  @apply transition-all ease-out duration-200;
}

/* do not animate the exiting element */
.list-leave-active {
  @apply duration-0;
}

.list-enter-from {
  @apply opacity-0 -translate-y-4;
}

/* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. Needed even if exiting item
   is not animated in order for the remaining items to move */
.list-leave-active {
  @apply fixed;
}
</style>
