<template>
  <div :class="{ 'text-sm': true, 'sm:table': true, 'w-full': true, '!hidden': !rows?.length }">
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
        <div class="sm:table-cell ca-cell">
          <div class="sm:hidden ca-xs-title">
            Quantité par DJR (en {{ payload.computedSubstances[rowIndex].substance.unit }})
          </div>
          <DsfrInputGroup class="max-w-28" v-if="!props.readonly">
            <DsfrInput
              v-model="payload.computedSubstances[rowIndex].quantity"
              label="Quantité par DJR"
              :required="true"
            />
          </DsfrInputGroup>
          <div v-else>{{ payload.computedSubstances[rowIndex].quantity }}</div>
        </div>
        <div class="hidden sm:table-cell fr-text-alt ca-cell font-italic">
          {{ payload.computedSubstances[rowIndex].substance.unit }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineModel, watch } from "vue"

const payload = defineModel()
const props = defineProps({ readonly: Boolean })

const headers = ["Nom", "Num CAS", "Num EINEC", "Ingrédient(s) source", "Qté par DJR", "Unité"]
const rows = computed(() =>
  payload.value.computedSubstances.map((x) => [
    x.substance.name.toLowerCase(),
    x.substance.casNumber || "-",
    x.substance.einecNumber || "-",
    sourceElements(x.substance),
  ])
)

const elements = computed(() =>
  [].concat(
    payload.value.declaredPlants,
    payload.value.declaredMicroorganisms,
    payload.value.declaredIngredients,
    payload.value.declaredSubstances
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
        payload.value.computedSubstances.push({ substance: newSubstance })
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
