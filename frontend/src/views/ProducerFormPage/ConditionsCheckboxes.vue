<template>
  <DsfrFieldset
    legend="Population à risque, facteurs de risque"
    hint="La consommation du complément alimentaire est déconseillée pour ces populations."
    legendClass="fr-label"
  >
    <div v-for="(section, index) in conditionsSections" class="mb-6 last:mb-0" :key="`condition-section-${index}`">
      <p class="font-bold mb-2">{{ section.title }}</p>
      <div class="grid grid-cols-6 gap-4 fr-checkbox-group input">
        <div
          v-for="condition in section.items"
          :key="`condition-${condition.id}`"
          class="flex col-span-6 sm:col-span-3 lg:col-span-2"
        >
          <input :id="`condition-${condition.id}`" type="checkbox" v-model="modelValue" :value="condition.id" />
          <label :for="`condition-${condition.id}`" class="fr-label">{{ condition.name }}</label>
        </div>
      </div>
    </div>
  </DsfrFieldset>
</template>

<script setup>
import { computed } from "vue"
import { transformArrayByColumn, checkboxColumnNumbers } from "@/utils/forms"
import { useCurrentBreakpoint } from "@/utils/screen"
import { populationCategoriesMapping } from "@/utils/mappings"

const currentBreakpoint = useCurrentBreakpoint()
const numberOfColumns = computed(() => checkboxColumnNumbers[currentBreakpoint.value])
const modelValue = defineModel()
const props = defineProps({ conditions: { type: Array, default: Array } })

const ageSort = (a, b) => a.maxAge - b.maxAge
const alphabeticalSort = (a, b) => a.name.localeCompare(b.name)

const conditionsSections = computed(() => {
  const c = props.conditions
  const cols = numberOfColumns.value
  return [
    {
      title: populationCategoriesMapping.AGE.label,
      items: transformArrayByColumn(c?.filter((x) => x.category === "AGE").sort(ageSort), cols),
    },
    {
      title: populationCategoriesMapping.MEDICAL.label,
      items: transformArrayByColumn(c?.filter((x) => x.category === "MEDICAL").sort(alphabeticalSort), cols),
    },
    {
      title: populationCategoriesMapping.PREGNANCY.label,
      items: transformArrayByColumn(c?.filter((x) => x.category === "PREGNANCY").sort(alphabeticalSort), cols),
    },
    {
      title: populationCategoriesMapping.MEDICAMENTS.label,
      items: transformArrayByColumn(c?.filter((x) => x.category === "MEDICAMENTS").sort(alphabeticalSort), cols),
    },
    {
      title: populationCategoriesMapping.OTHER.label,
      items: transformArrayByColumn(c?.filter((x) => x.category === "OTHER").sort(alphabeticalSort), cols),
    },
  ]
})
</script>
