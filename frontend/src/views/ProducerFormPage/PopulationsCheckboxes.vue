<template>
  <div class="mb-6">
    <h3 class="fr-label mb-4">Population cible</h3>
    <DsfrFieldset
      v-for="(section, index) in populationsSections"
      class="mb-2"
      :key="`pop-section-${index}`"
      legendClass="pb-2"
    >
      <template #legend>
        <span class="sr-only">Population cible,</span>
        {{ section.title }}
      </template>
      <div class="grid grid-cols-6 gap-4 fr-checkbox-group input">
        <div
          v-for="population in section.items"
          :key="`pop-${population.id}`"
          class="flex col-span-6 sm:col-span-3 lg:col-span-2"
        >
          <input :id="`population-${population.id}`" type="checkbox" v-model="modelValue" :value="population.id" />
          <label :for="`population-${population.id}`" class="fr-label">{{ population.name }}</label>
        </div>
      </div>
    </DsfrFieldset>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { transformArrayByColumn, checkboxColumnNumbers } from "@/utils/forms"
import { useCurrentBreakpoint } from "@/utils/screen"
import { populationCategoriesMapping } from "@/utils/mappings"

const currentBreakpoint = useCurrentBreakpoint()
const numberOfColumns = computed(() => checkboxColumnNumbers[currentBreakpoint.value])
const modelValue = defineModel()
const props = defineProps({ populations: { type: Array, default: Array } })

const ageSort = (a, b) => a.maxAge - b.maxAge
const alphabeticalSort = (a, b) => a.name.localeCompare(b.name)

const populationsSections = computed(() => {
  const p = props.populations
  const cols = numberOfColumns.value
  return [
    {
      title: populationCategoriesMapping.AGE.label,
      items: transformArrayByColumn(p?.filter((x) => x.category === "AGE").sort(ageSort), cols),
    },
    {
      title: populationCategoriesMapping.PREGNANCY.label,
      items: transformArrayByColumn(p?.filter((x) => x.category === "PREGNANCY").sort(alphabeticalSort), cols),
    },
    {
      title: populationCategoriesMapping.OTHER.label,
      items: transformArrayByColumn(p?.filter((x) => x.category === "OTHER").sort(alphabeticalSort), cols),
    },
  ]
})
</script>
