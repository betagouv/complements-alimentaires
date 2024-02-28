<template>
  <div class="block text-sm sm:table w-full">
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
    <div class="block sm:table-row-group">
      <div
        class="block sm:table-row border sm:border-0 p-2 sm:p-0 mb-2 sm:mb-0"
        v-for="(row, rowIndex) in rows"
        :key="`row-${rowIndex}`"
      >
        <!-- Cells contenant l'information de la substance -->
        <div
          class="block sm:table-cell ca-cell capitalize"
          v-for="(item, cellIndex) in row"
          :key="`cell-${rowIndex}-${cellIndex}`"
        >
          <div class="block sm:hidden ca-xs-title">
            {{ headers[cellIndex] }}
          </div>
          <div>{{ item }}</div>
        </div>

        <!-- Cells des inputs (communes à toutes les substances) -->
        <div class="block sm:table-cell ca-cell">
          <div class="block sm:hidden ca-xs-title">Quantité par DJR (en mg)</div>
          <DsfrInputGroup class="max-w-28">
            <DsfrInput v-model="payload.substances[rowIndex].quantity" label="Quantité par DJR" :required="true" />
          </DsfrInputGroup>
        </div>
        <div class="hidden sm:table-cell fr-text-alt ca-cell font-italic">mg</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineModel, watch } from "vue"

const payload = defineModel()
const headers = ["Nom", "Num CAS", "Num EINEC", "Ingrédient(s) source", "Qté / DJR", "Unité"]
const rows = computed(() =>
  payload.value.substances.map((x) => [
    x.substance.name.toLowerCase(),
    x.substance.casNumber || "-",
    x.substance.einecNumber || "-",
    sourceElements(x.substance),
  ])
)

const elements = computed(() => payload.value.elements)

const sourceElements = (substance) => {
  const sources = elements.value.filter(
    (x) => x.element.objectType === "substance" || x.element.substances.indexOf(substance) > -1
  )
  return sources.map((x) => x.element.name).join(", ")
}

watch(
  elements,
  () => {
    const newSubstances = elements.value
      .map((x) => (x.element.objectType === "substance" ? [x.element] : x.element.substances))
      .flat()
      .filter((x) => !!x)

    // Ajouter les nouvelles substances
    newSubstances.forEach((newSubstance) => {
      if (!payload.value.substances.find((x) => x.substance.id === newSubstance.id))
        payload.value.substances.push({ substance: newSubstance })
    })

    // Enlever les substances disparues
    const outdatedElementIndexes = []
    payload.value.substances.forEach((item, index) => {
      if (!newSubstances.find((x) => (x.id = item.substance.id))) outdatedElementIndexes.push(index)
    })
    outdatedElementIndexes.forEach((index) => payload.value.substances.splice(index, 1))
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
