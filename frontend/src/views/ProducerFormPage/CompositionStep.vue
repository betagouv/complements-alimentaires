<template>
  <h2 class="fr-h6">
    <v-icon class="mr-1" name="ri-flask-line" />
    Ma composition
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
    <div class="mt-4 sm:mt-0"><NewElementModal @add="addElement" /></div>
  </div>

  <ElementList @remove="removeElement" objectType="plant" :elements="payload.declaredPlants" />
  <ElementList @remove="removeElement" objectType="microorganism" :elements="payload.declaredMicroorganisms" />
  <ElementList @remove="removeElement" objectType="ingredient" :elements="payload.declaredIngredients" />
  <ElementList @remove="removeElement" objectType="substance" :elements="payload.declaredSubstances" />
  <div v-if="allElements.length === 0" class="my-12">
    <v-icon name="ri-information-line" class="mr-1"></v-icon>
    Vous n'avez pas encore saisi d'ingrédients pour votre complément alimentaire
  </div>

  <div :class="{ hidden: !hasActiveElements }">
    <h3 class="fr-h6 !mb-4 !mt-6">Substances</h3>
    <p>
      Les substances contenues dans les ingrédients actifs renseignés sont affichées ci-dessous. Veuillez compléter leur
      dosage total.
    </p>
    <SubstancesTable v-model="payload" />
  </div>
</template>

<script setup>
import { ref, watch, computed, defineModel } from "vue"
import { useFetch, useDebounceFn } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import ElementList from "./ElementList.vue"
import SubstancesTable from "./SubstancesTable.vue"
import NewElementModal from "./NewElementModal.vue"
import useToaster from "@/composables/use-toaster"
import { handleError } from "@/utils/error-handling"

const payload = defineModel()

const autocompleteResults = ref([])
const searchTerm = ref("")
const debounceDelay = 350
const containers = {
  plant: payload.value.declaredPlants,
  microorganism: payload.value.declaredMicroorganisms,
  ingredient: payload.value.declaredIngredients,
  substance: payload.value.declaredSubstances,
}
// Ce tableau nous sert à afficher les éléments dans une seule liste par type
// et par ordre alphabétique
const allElements = computed(() => [].concat(...Object.values(containers)))
const hasActiveElements = computed(() => allElements.value.some((x) => x.active && !x.new))

const selectOption = async (result) => {
  searchTerm.value = ""
  autocompleteResults.value = []
  const item = await fetchElement(result.objectType, result.id)
  addElement(item, result.objectType)
}

const removeElement = (element) => {
  Object.values(containers).forEach((container) => {
    const index = container.indexOf(element)
    if (index > -1) container.splice(index, 1)
  })
}
const addElement = (item, objectType, newlyAdded = false) => {
  // Pour l'instant on met `active: true` mais une fois qu'on intègrera les additifs, il faudra
  // ajouter un peu de logique car les additifs sont par défaut "non actifs". Potentiellement
  // ils ne pourront jamais devenir "actifs" d'un point de vue métier.
  const toAdd = newlyAdded ? { ...item, ...{ active: true, new: true } } : { element: item, active: true }
  containers[objectType].unshift(toAdd)
}

const fetchAutocompleteResults = useDebounceFn(async () => {
  if (searchTerm.value.length < 3) {
    autocompleteResults.value = []
    return
  }

  const body = { term: searchTerm.value }
  const { error, data } = await useFetch("/api/v1/elements/autocomplete/", { headers: headers() }).post(body).json()

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
  const { data, response } = await useFetch(`/api/v1/${type}s/${id}`).get().json()
  await handleError(response)
  if (!response.value.ok) return null
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
