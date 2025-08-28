<template>
  <DsfrAlert v-if="ingredientsRequiringAnalysisReport.length" small class="mb-4">
    <p>Un bulletin d'analyse est nécessaire pour l'utilisation des ingrédients suivants :</p>
    <ul class="mb-0">
      <li v-for="ingredient in ingredientsRequiringAnalysisReport" :key="`${ingredient.type}-${ingredient.id}`">
        {{ ingredient.element.name }}
      </li>
    </ul>
  </DsfrAlert>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps(["declaration"])

const ingredientsRequiringAnalysisReport = computed(() => {
  return []
    .concat(
      props.declaration.declaredPlants,
      props.declaration.declaredMicroorganisms,
      props.declaration.declaredIngredients,
      props.declaration.declaredSubstances
    )
    .filter((x) => x.element?.requiresAnalysisReport)
})
</script>
