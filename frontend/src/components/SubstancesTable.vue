<template>
  <div class="text-sm sm:table w-full" v-show="rows?.length">
    <div class="hidden sm:table-header-group bg-gray-100">
      <div class="table-row">
        <div
          class="table-cell border-b-2 border-black font-bold p-4"
          v-for="(header, index) in headers"
          :key="`header-${index}`"
        >
          {{ header }}
        </div>
      </div>
    </div>
    <div class="sm:table-row-group">
      <div
        class="sm:table-row border sm:border-0 p-2 sm:p-0 mb-2 sm:mb-0"
        v-for="(row, rowIndex) in rows"
        :key="`row-${rowIndex}`"
      >
        <div class="sm:table-cell ca-cell">
          <ElementCommentModal
            :hidePrivateComments="hidePrivateComments"
            v-model="payload.computedSubstances[rowIndex]"
          />
        </div>
        <!-- Cells contenant l'information de la substance -->
        <div
          class="sm:table-cell ca-cell capitalize"
          v-for="(item, cellIndex) in row"
          :key="`cell-${rowIndex}-${cellIndex}`"
        >
          <div class="sm:hidden ca-xs-title">
            {{ headers[cellIndex] }}
          </div>
          <div>{{ item }}</div>
        </div>

        <!-- Cells des inputs (communes à toutes les substances) -->
        <div class="sm:table-cell ca-cell sm:max-w-16">
          <div class="sm:hidden ca-xs-title">
            Quantité par DJR (en {{ payload.computedSubstances[rowIndex].substance.unit }})
          </div>
          <div v-if="props.readonly">
            {{ payload.computedSubstances[rowIndex].quantity }}
          </div>
          <div
            :class="{
              '!text-red-marianne-425 font-bold': getMaxQuantityExceeded(payload.computedSubstances[rowIndex]),
            }"
            v-if="getMaxQuantityExceeded(payload.computedSubstances[rowIndex])"
          >
            ({{ getMaxQuantityExceeded(payload.computedSubstances[rowIndex]) }})
          </div>
          <DsfrInputGroup v-else>
            <NumberField
              v-model="payload.computedSubstances[rowIndex].quantity"
              label="Quantité par DJR"
              :required="payload.computedSubstances[rowIndex].substance.mustSpecifyQuantity"
            />
            <div
              class="!text-neutral-500 mt-1"
              v-if="payload.computedSubstances[rowIndex].substance.mustSpecifyQuantity"
            >
              * champ obligatoire
            </div>
          </DsfrInputGroup>
        </div>
        <div class="hidden sm:table-cell fr-text-alt ca-cell font-italic">
          <span>
            {{ payload.computedSubstances[rowIndex].substance.unit }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// TODO: Convertir dans une DSFRTable

import { computed, watch } from "vue"
import ElementCommentModal from "@/components/ElementCommentModal"
import NumberField from "@/components/NumberField"
import { storeToRefs } from "pinia"
import { useRootStore } from "@/stores/root"

const store = useRootStore()
const { populations } = storeToRefs(store)

const payload = defineModel()
const props = defineProps({ readonly: Boolean, hidePrivateComments: Boolean })

const headers = ["", "Nom", "Ingrédient(s) source", "Qté totale par DJR", "Unité"]
const rows = computed(() =>
  payload.value.computedSubstances.map((x) => [x.substance.name.toLowerCase(), sourceElements(x.substance)])
)

const elements = computed(() =>
  [].concat(
    payload.value.declaredPlants,
    payload.value.declaredMicroorganisms,
    payload.value.declaredIngredients,
    payload.value.declaredSubstances
    // Aromas et Additives ne sont pas actif et ne sont donc pas liés à des substances actives
  )
)
const activeElements = computed(() => elements.value.filter((x) => x.active && !x.new))

const sourceElements = (substance) => {
  const sources = activeElements.value.filter(
    (x) =>
      (x.element.objectType === "substance" && x.element.id === substance.id) ||
      x.element.substances?.map((item) => item.id).indexOf(substance.id) > -1
  )
  return sources.map((x) => x.element.name).join(", ")
}

const getMaxQuantityExceeded = (declaredOrComputedSubstance) => {
  const findName = (id) => populations.value?.find((y) => y.id === id)?.name
  const exceeded_population_quantity = declaredOrComputedSubstance.substance.maxQuantities.filter(
    (maxQuantityPerPopulation) =>
      payload.value.populations.indexOf(parseInt(maxQuantityPerPopulation.population)) != -1 &&
      declaredOrComputedSubstance.quantity > maxQuantityPerPopulation.maxQuantity
  )

  const exceeded_populations = exceeded_population_quantity.length
    ? exceeded_population_quantity.map((maxQuantityPerPopulation) =>
        findName(parseInt(maxQuantityPerPopulation.population))
      )
    : ["Population générale"]
  let max_quantity = 0
  if (exceeded_population_quantity.length) {
    exceeded_population_quantity.forEach((maxQuantityPerPopulation) => {
      if (maxQuantityPerPopulation.maxQuantity > max_quantity) {
        max_quantity = maxQuantityPerPopulation.maxQuantity
      }
    })
  } else max_quantity = declaredOrComputedSubstance.substance.maxQuantity
  if (exceeded_populations.length) return max_quantity + " maximum autorisé pour " + exceeded_populations.join(", ")
  else return
}
watch(
  elements,
  () => {
    const newSubstances = activeElements.value
      .map((x) => (x.element.objectType === "substance" ? [x.element] : x.element.substances))
      .flat()
      .filter((x) => !!x)

    // Ajouter les nouvelles substances
    newSubstances.forEach((newSubstance) => {
      if (!payload.value.computedSubstances.find((x) => x.substance.id === newSubstance.id))
        payload.value.computedSubstances.push({ substance: newSubstance, unit: newSubstance.unitId })
    })

    // Enlever les substances disparues
    payload.value.computedSubstances = payload.value.computedSubstances.filter((item) =>
      newSubstances.find((x) => x.id === item.substance.id)
    )
  },
  { deep: true, immediate: true }
)
</script>

<style scoped>
.ca-cell {
  @apply align-middle p-0 sm:p-2 border-0 sm:border-b;
}

.ca-xs-title {
  @apply font-bold my-2;
}
</style>
