<template>
  <div class="bg-blue-france-975 border border-slate-300">
    <div class="fr-container pt-4 pb-6">
      <DsfrStepper class="!mb-0" :currentStep="currentStep" :steps="steps" />
    </div>
  </div>
  <div class="fr-container mt-8 mb-10">
    <component :is="components[currentStep - 1]"></component>
  </div>
</template>
<script setup>
import { ref } from "vue"
import ProductStep from "./ProductStep"
import CompositionStep from "./CompositionStep"

const currentStep = ref(1)
const steps = ["Le produit", "La composition", "Description", "Résumé"]
const components = [ProductStep, CompositionStep, ProductStep, ProductStep]
</script>
