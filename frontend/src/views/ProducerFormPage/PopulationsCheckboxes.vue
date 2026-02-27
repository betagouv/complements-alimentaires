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
      <div class="fr-checkbox-group input md:columns-2 lg:columns-3">
        <div v-for="population in section.items" :key="`pop-${population.id}`" class="flex mb-4 last:mb-0">
          <input :id="`population-${population.id}`" type="checkbox" v-model="modelValue" :value="population.id" />
          <label :for="`population-${population.id}`" class="fr-label">{{ population.name }}</label>
        </div>
      </div>
    </DsfrFieldset>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { populationCategoriesMapping } from "@/utils/mappings"

const modelValue = defineModel()
const props = defineProps({ populations: { type: Array, default: Array } })

const ageSort = (a, b) => a.maxAge - b.maxAge

const populationsSections = computed(() => {
  const p = props.populations
  return [
    {
      title: populationCategoriesMapping.AGE.label,
      items: p?.filter((x) => x.category === "AGE").sort(ageSort),
    },
    {
      title: populationCategoriesMapping.PREGNANCY.label,
      items: p?.filter((x) => x.category === "PREGNANCY"),
    },
    {
      title: populationCategoriesMapping.OTHER.label,
      items: p?.filter((x) => x.category === "OTHER"),
    },
  ]
})
</script>
