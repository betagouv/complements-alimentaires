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
        :hideSearchButton="true"
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
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'form_of_supply')"
    />
    <ElementList
      @remove="removeElement"
      objectType="aroma"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'aroma')"
    />
    <ElementList
      @remove="removeElement"
      objectType="additive"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'additive')"
    />
    <ElementList
      @remove="removeElement"
      objectType="active_ingredient"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'active_ingredient')"
    />
    <ElementList
      @remove="removeElement"
      objectType="non_active_ingredient"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'non_active_ingredient')"
    />
    <ElementList @remove="removeElement" objectType="substance" :elements="payload.declaredSubstances" />
    <!-- On conserve ce type ingredient déprécié temporairement -->
    <ElementList
      @remove="removeElement"
      objectType="ingredient"
      :elements="getObjectSubTypeList(payload.declaredIngredients, null)"
    />

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
      <SubstancesTable :hidePrivateComments="true" v-model="payload" />
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useFetch } from "@vueuse/core"
import { getApiType, getActivityByType } from "@/utils/mappings"
import { getObjectSubTypeList } from "@/utils/elements"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import ElementList from "./ElementList.vue"
import SubstancesTable from "@/components/SubstancesTable.vue"
import NewElementModal from "./NewElementModal.vue"
import { handleError } from "@/utils/error-handling"
import SectionTitle from "@/components/SectionTitle"
import useToaster from "@/composables/use-toaster"

const payload = defineModel()
const containers = computed(() => ({
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
}))
const allElements = computed(() =>
  [].concat(
    ...[
      payload.value.declaredPlants,
      payload.value.declaredMicroorganisms,
      payload.value.declaredSubstances,
      payload.value.declaredIngredients,
    ]
  )
)
const hasActiveSubstances = computed(() =>
  allElements.value.some(
    (x) => x.active && !x.new && (x.element?.substances?.length || containers.value.substance.indexOf(x) > -1)
  )
)

const selectOption = async (result) => {
  const item = await fetchElement(getApiType(result.objectType), result.objectType, result.id)
  addElement(item, result.objectType)
}

const removeElement = (element) => {
  Object.values(containers.value).forEach((container) => {
    const index = container.indexOf(element)
    if (index > -1) container.splice(index, 1)
  })
}
const addElement = (item, objectType, newlyAdded = false) => {
  const itemExists = item.id && allElements.value.find((x) => x.element?.id === item.id)
  if (itemExists) {
    useToaster().addSuccessMessage("L'ingrédient est déjà présent dans votre composition.")
    return
  }
  const toAdd = newlyAdded
    ? {
        ...item,
        ...{ active: getActivityByType(objectType), new: true, activated: true, newType: objectType },
      }
    : { element: item, active: !!item.activity, activated: true }
  //  le champ activated n'est valable que pour les microorganismes
  containers.value[objectType].unshift(toAdd)
}

const fetchElement = async (apiType, type, id) => {
  const { data, response } = await useFetch(`/api/v1/${apiType}s/${id}`).get().json()
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
