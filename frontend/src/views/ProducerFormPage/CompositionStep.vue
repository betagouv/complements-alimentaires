<template>
  <div>
    <SectionTitle title="Ma composition" sizeTag="h6" icon="ri-flask-line" />
    <div class="sm:flex gap-10 items-center">
      <ElementAutocomplete
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

    <div v-show="hasActiveSubstances">
      <h3 class="fr-h6 !mb-4 !mt-6">Substances</h3>
      <p>
        Les substances contenues dans les ingrédients actifs renseignés sont affichées ci-dessous. Veuillez compléter
        leur dosage total.
      </p>
      <SubstancesTable v-model="payload" />
    </div>
  </div>
</template>

<script setup>
import { computed, defineModel } from "vue"
import { useFetch } from "@vueuse/core"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import ElementList from "./ElementList.vue"
import SubstancesTable from "@/components/SubstancesTable.vue"
import NewElementModal from "./NewElementModal.vue"
import { handleError } from "@/utils/error-handling"
import SectionTitle from "@/components/SectionTitle"

const payload = defineModel()
const containers = {
  plant: payload.value.declaredPlants,
  microorganism: payload.value.declaredMicroorganisms,
  ingredient: payload.value.declaredIngredients,
  substance: payload.value.declaredSubstances,
}
const allElements = computed(() => [].concat(...Object.values(containers)))
const hasActiveSubstances = computed(() =>
  allElements.value.some((x) => x.active && !x.new && x.element?.substances?.length)
)

const selectOption = async (result) => {
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

const fetchElement = async (type, id) => {
  const { data, response } = await useFetch(`/api/v1/${type}s/${id}`).get().json()
  await handleError(response)
  if (!response.value.ok) return null
  return { ...data.value, ...{ objectType: type } }
}
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
