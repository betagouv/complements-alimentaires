<template>
  <h2 class="fr-h6">
    <v-icon class="mr-1" name="ri-flask-line" />
    Ingrédients
  </h2>
  <div class="sm:flex gap-10 items-center">
    <ElementAutocomplete
      v-model="searchTerm"
      :options="autocompleteResults"
      autocomplete="nothing"
      label="Cherchez un ingrédient"
      label-visible
      class="max-w-md grow"
      hint="Tapez au moins trois caractères pour démarrer la recherche"
      @selected="selectOption"
    />
    <div class="hidden sm:flex flex-col items-center">
      <div class="border-l h-6"></div>
      <div class="my-2">Ou</div>
      <div class="border-l h-6"></div>
    </div>
    <div class="mt-4 sm:mt-0"><NewElementModal @add="addNewElement" /></div>
  </div>
  <TransitionGroup mode="out-in" name="list" tag="div" class="mt-8 relative">
    <ElementCard
      v-for="(element, index) in payload.elements"
      :key="`element-${element.id}`"
      @remove="removeElement(index)"
      v-model="payload.elements[index]"
      class="mb-2"
    />
  </TransitionGroup>
  <div v-if="payload.elements.length === 0" class="my-12">
    <v-icon name="ri-information-line" class="mr-1"></v-icon>
    Vous n'avez pas encore saisi d'ingrédients pour votre complément alimentaire
  </div>

  <div v-if="hasActiveElements">
    <h3 class="fr-h6 !mb-4 !mt-6">Substances</h3>
    <p>
      Les substances contenues dans les ingrédients actifs renseignés sont affichées ci-dessous. Veuillez compléter leur
      dosage.
    </p>
    <SubstancesTable v-model="payload" />
  </div>
</template>

<script setup>
import { ref, watch, computed, defineModel } from "vue"
import { useFetch, useDebounceFn } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import ElementCard from "./ElementCard.vue"
import SubstancesTable from "./SubstancesTable.vue"
import NewElementModal from "./NewElementModal.vue"
import useToaster from "@/composables/use-toaster"

const payload = defineModel()

const autocompleteResults = ref([])
const searchTerm = ref("")
const debounceDelay = 350

const selectOption = async (result) => {
  searchTerm.value = ""
  autocompleteResults.value = []
  const item = { element: await fetchElement(result.objectType, result.id) }
  payload.value.elements.unshift(item)
}

const removeElement = (index) => payload.value.elements.splice(index, 1)
const hasActiveElements = computed(() => payload.value.elements.some((x) => x.element.active))

const addNewElement = (element) => console.log(element)

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
  // Pour l'instant on met `active: true` mais une fois qu'on intègrera les additifs, il faudra
  // ajouter un peu de logique car les additifs sont par défaut "non actifs". Potentiellement
  // ils ne pourront jamais devenir "actifs" d'un point de vue métier.
  return { ...data.value, ...{ objectType: type, active: true } }
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
