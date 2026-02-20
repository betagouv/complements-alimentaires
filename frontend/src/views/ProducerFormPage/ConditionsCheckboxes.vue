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
      <div class="fr-checkbox-group input md:columns-2 lg:columns-3">
        <div v-for="condition in section.items" :key="`condition-${condition.id}`" class="flex mb-4 last:mb-0">
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
import { populationCategoriesMapping } from "@/utils/mappings"

const modelValue = defineModel()
const props = defineProps({ conditions: { type: Array, default: Array } })

const ageSort = (a, b) => a.maxAge - b.maxAge

const conditionsSections = computed(() => {
  const c = props.conditions
  return [
    {
      title: populationCategoriesMapping.AGE.label,
      items: c?.filter((x) => x.category === "AGE").sort(ageSort),
    },
    {
      title: populationCategoriesMapping.MEDICAL.label,
      items: c?.filter((x) => x.category === "MEDICAL"),
    },
    {
      title: populationCategoriesMapping.PREGNANCY.label,
      items: c?.filter((x) => x.category === "PREGNANCY"),
    },
    {
      title: populationCategoriesMapping.MEDICAMENTS.label,
      items: c?.filter((x) => x.category === "MEDICAMENTS"),
    },
    {
      title: populationCategoriesMapping.OTHER.label,
      items: c?.filter((x) => x.category === "OTHER"),
      isOtherSection: true,
    },
  ]
})
</script>
