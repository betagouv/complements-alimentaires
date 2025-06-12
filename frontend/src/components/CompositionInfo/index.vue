<template>
  <div>
    <SummaryElementList
      :useAccordions="useAccordions"
      :showElementAuthorization="showElementAuthorization"
      objectType="plant"
      :elements="payload.declaredPlants"
    />
    <SummaryElementList
      :useAccordions="useAccordions"
      :showElementAuthorization="showElementAuthorization"
      objectType="microorganism"
      :elements="payload.declaredMicroorganisms"
    />
    <SummaryElementList
      objectType="form_of_supply"
      :useAccordions="useAccordions"
      :showElementAuthorization="showElementAuthorization"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'form_of_supply')"
    />
    <SummaryElementList
      :useAccordions="useAccordions"
      :showElementAuthorization="showElementAuthorization"
      objectType="aroma"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'aroma')"
    />
    <SummaryElementList
      objectType="additive"
      :useAccordions="useAccordions"
      :showElementAuthorization="showElementAuthorization"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'additive')"
    />
    <SummaryElementList
      objectType="active_ingredient"
      :useAccordions="useAccordions"
      :showElementAuthorization="showElementAuthorization"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'active_ingredient')"
    />
    <SummaryElementList
      objectType="non_active_ingredient"
      :useAccordions="useAccordions"
      :showElementAuthorization="showElementAuthorization"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'non_active_ingredient')"
    />
    <SummaryElementList
      objectType="substance"
      :useAccordions="useAccordions"
      :showElementAuthorization="showElementAuthorization"
      :elements="payload.declaredSubstances"
    />
  </div>
</template>

<script setup>
import { getObjectSubTypeList } from "@/utils/elements"
import SummaryElementList from "./SummaryElementList"

const payload = defineModel()

defineProps({ useAccordions: Boolean, showElementAuthorization: Boolean })
</script>
