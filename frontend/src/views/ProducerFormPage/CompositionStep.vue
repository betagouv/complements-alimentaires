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
    <ElementList
      @remove="removeElement"
      objectType="form_of_supply"
      :elements="payload.declaredIngredients.filter((obj) => obj.element.objectType == 'form_of_supply')"
    />
    <ElementList
      @remove="removeElement"
      objectType="aroma"
      :elements="payload.declaredIngredients.filter((obj) => obj.element.objectType == 'aroma')"
    />
    <ElementList
      @remove="removeElement"
      objectType="additive"
      :elements="payload.declaredIngredients.filter((obj) => obj.element.objectType == 'additive')"
    />
    <ElementList
      @remove="removeElemenpropertyt"
      objectType="active_ingredient"
      :elements="payload.declaredIngredients.filter((obj) => obj.element.objectType == 'active_ingredient')"
    />
    <ElementList
      @remove="removeElement"
      objectType="non_active_ingredient"
      :elements="payload.declaredIngredients.filter((obj) => obj.element.objectType == 'non_active_ingredient')"
    />
    <ElementList @remove="removeElement" objectType="substance" :elements="payload.declaredSubstances" />
    <!-- On conserve ce type ingredient déprécié temporairement -->
    <!-- <ElementList @remove="removeElement" objectType="ingredient" :elements="payload.declaredIngredients" /> -->

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
import { getApiType, getActivityNotEditableByType } from "@/utils/mappings"
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
  substance: payload.value.declaredSubstances,
  // ingredient contient [aromas, addives, form_of_supply, others_ingredients]
  form_of_supply: payload.value.declaredIngredients,
  aroma: payload.value.declaredIngredients,
  additive: payload.value.declaredIngredients,
  active_ingredient: payload.value.declaredIngredients,
  non_active_ingredient: payload.value.declaredIngredients,
  // TODO déprecier après l'import de données extraites en mai 2024
  // qui contient les types plus précis
  ingredient: payload.value.declaredIngredients,
}
const allElements = computed(() => [].concat(...Object.values(containers)))
const hasActiveSubstances = computed(() =>
  allElements.value.some((x) => x.active && !x.new && x.element?.substances?.length)
)

const selectOption = async (result) => {
  const item = await fetchElement(getApiType(result.objectType), result.id)
  addElement(item, result.objectType)
}

const removeElement = (element) => {
  Object.values(containers).forEach((container) => {
    const index = container.indexOf(element)
    if (index > -1) container.splice(index, 1)
  })
}
const addElement = (item, objectType, newlyAdded = false) => {
  // TODO : pour le moment les objets de type `plant` peuvent être ou non actif.
  // à terme toutes les plantes seront actives et si elles sont non actives c'est que ce sont des support/agent de charge
  const activityNotEditable = getActivityNotEditableByType(objectType)
  const toAdd = newlyAdded
    ? { ...item, ...{ active: item.activity, disabled: activityNotEditable, new: true } }
    : { element: item, active: item.activity, disabled: activityNotEditable }
  containers[objectType].unshift(toAdd)
}

const fetchElement = async (type, id) => {
  const { data, response } = await useFetch(`/api/v1/${type}s/${id}`).get().json()
  await handleError(response)
  if (!response.value.ok) return null
  return data.value
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
