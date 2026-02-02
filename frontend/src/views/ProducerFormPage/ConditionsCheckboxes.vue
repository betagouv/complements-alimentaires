<template>
  <div class="mb-8">
    <h3 class="fr-label mb-2">Population à risque, facteurs de risque</h3>
    <p class="fr-hint-text">La consommation du complément alimentaire est déconseillée pour ces populations.</p>
    <DsfrFieldset
      v-for="(section, index) in conditionsSections"
      class="mb-2"
      :key="`condition-section-${index}`"
      legendClass="pb-2"
    >
      <template #legend>
        <span class="sr-only">Population à risque, facteurs de risque,</span>
        {{ section.title }}
      </template>
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
      <slot v-if="section.isOtherSection"></slot>
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
const props = defineProps({ conditions: { type: Array, default: Array } })

const ageSort = (a, b) => a.maxAge - b.maxAge

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
      items: transformArrayByColumn(
        c?.filter((x) => x.category === "MEDICAL"),
        cols
      ),
    },
    {
      title: populationCategoriesMapping.PREGNANCY.label,
      items: transformArrayByColumn(
        c?.filter((x) => x.category === "PREGNANCY"),
        cols
      ),
    },
    {
      title: populationCategoriesMapping.MEDICAMENTS.label,
      items: transformArrayByColumn(
        c?.filter((x) => x.category === "MEDICAMENTS"),
        cols
      ),
    },
    {
      title: populationCategoriesMapping.OTHER.label,
      items: transformArrayByColumn(
        c?.filter((x) => x.category === "OTHER"),
        cols
      ),
      isOtherSection: true,
    },
  ]
})
</script>
