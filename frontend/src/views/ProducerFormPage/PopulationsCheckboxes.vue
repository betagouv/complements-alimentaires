<template>
  <DsfrFieldset legend="Population cible" legendClass="fr-label">
    <div v-for="(section, index) in populationsSections" :key="`pop-section-${index}`">
      <p class="mt-4 mb-2 font-bold">{{ section.title }}</p>
      <div class="grid grid-cols-6 gap-4 fr-checkbox-group input">
        <div
          v-for="population in section.items"
          :key="`effect-${population.id}`"
          class="flex col-span-6 sm:col-span-3 lg:col-span-2"
        >
          <input :id="`population-${population.id}`" type="checkbox" v-model="modelValue" :value="population.id" />
          <label :for="`population-${population.id}`" class="fr-label ml-2">{{ population.name }}</label>
        </div>
      </div>
    </div>
  </DsfrFieldset>
</template>

<script setup>
import { computed, watch, ref } from "vue"
import { transformArrayByColumn } from "@/utils/forms"
import { getCurrentBreakpoint } from "@/utils/screen"
import { useWindowSize } from "@vueuse/core"

const modelValue = defineModel()
const props = defineProps({ populations: { type: Array, default: Array } })

const populationsSections = computed(() => {
  const p = props.populations
  return [
    {
      title: "Âge",
      items: transformArrayByColumn(
        p.filter((x) => x.category === "AGE").sort((a, b) => a.minAge - b.minAge),
        numberOfColumns.value
      ),
    },
    {
      title: "Conditions médicales spécifiques",
      items: transformArrayByColumn(
        p.filter((x) => x.category === "MEDICAL").sort((a, b) => a.name.localeCompare(b.name)),
        numberOfColumns.value
      ),
    },
    {
      title: "Grossesse et allaitement",
      items: transformArrayByColumn(
        p.filter((x) => x.category === "PREGNANCY").sort((a, b) => a.name.localeCompare(b.name)),
        numberOfColumns.value
      ),
    },
    {
      title: "Autres",
      items: transformArrayByColumn(
        p.filter((x) => x.category === "OTHER").sort((a, b) => a.name.localeCompare(b.name)),
        numberOfColumns.value
      ),
    },
  ]
})

const { width } = useWindowSize()
const numberOfColumns = ref()
watch(
  width,
  () => {
    const checkboxColumnNumbers = { sm: 1, md: 2, lg: 2, xl: 3 }
    numberOfColumns.value = checkboxColumnNumbers[getCurrentBreakpoint()] || 1
  },
  { immediate: true }
)
const orderedPopulations = computed(() => transformArrayByColumn(props.populations, numberOfColumns.value))
</script>
