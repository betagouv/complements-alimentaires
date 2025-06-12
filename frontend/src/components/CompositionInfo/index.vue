<template>
  <div>
    <SummaryElementList
      :useAccordions="useAccordions"
      :showElementAuthorization="showElementAuthorization"
      :objectType="section.objectType"
      :elements="section.elements"
      v-for="section in sections"
      :key="section.objectType"
    />
  </div>
</template>

<script setup>
import { getObjectSubTypeList } from "@/utils/elements"
import SummaryElementList from "./SummaryElementList"
import { computed } from "vue"

const payload = defineModel()

defineProps({ useAccordions: Boolean, showElementAuthorization: Boolean })

const sections = computed(() => [
  {
    elements: payload.value.declaredPlants,
    objectType: "plant",
  },
  {
    elements: payload.value.declaredMicroorganisms,
    objectType: "microorganism",
  },
  {
    elements: getObjectSubTypeList(payload.value.declaredIngredients, "form_of_supply"),
    objectType: "form_of_supply",
  },
  {
    elements: getObjectSubTypeList(payload.value.declaredIngredients, "aroma"),
    objectType: "aroma",
  },
  {
    elements: getObjectSubTypeList(payload.value.declaredIngredients, "additive"),
    objectType: "additive",
  },
  {
    elements: getObjectSubTypeList(payload.value.declaredIngredients, "active_ingredient"),
    objectType: "active_ingredient",
  },
  {
    elements: getObjectSubTypeList(payload.value.declaredIngredients, "non_active_ingredient"),
    objectType: "non_active_ingredient",
  },
  {
    elements: payload.value.declaredSubstances,
    objectType: "substance",
  },
])
</script>
