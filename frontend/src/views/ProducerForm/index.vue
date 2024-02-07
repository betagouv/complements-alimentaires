<template>
  <div class="bg-blue-france-975 border border-slate-300">
    <div class="fr-container pt-4 pb-6">
      <DsfrStepper class="!mb-0" :currentStep="currentStep" :steps="steps" />
    </div>
  </div>
  <div class="fr-container">
    <div class="flex mb-6 mt-3 p-3 justify-end border rounded-md">
      <DsfrButton
        icon="ri-arrow-left-line"
        class="mr-3"
        label="Précedent"
        @click="() => (currentStep -= 1)"
        size="small"
        :disabled="currentStep === 1"
      />
      <DsfrButton
        icon="ri-arrow-right-line"
        label="Suivant"
        @click="() => (currentStep += 1)"
        size="small"
        :disabled="currentStep === steps.length"
      />
    </div>
    <component :is="components[currentStep - 1]"></component>
    <div class="flex mb-3 mt-6 p-3 justify-end border rounded-md">
      <DsfrButton
        icon="ri-arrow-left-line"
        class="mr-3"
        label="Précedent"
        @click="() => (currentStep -= 1)"
        size="small"
        :disabled="currentStep === 1"
      />
      <DsfrButton
        icon="ri-arrow-right-line"
        label="Suivant"
        @click="() => (currentStep += 1)"
        size="small"
        :disabled="currentStep === steps.length"
      />
    </div>
  </div>
</template>
<script setup>
import { ref } from "vue"
import ProductStep from "./ProductStep"
import CompositionStep from "./CompositionStep"
import SummaryStep from "./SummaryStep"
import AttachmentStep from "./AttachmentStep"

const currentStep = ref(1)
const steps = ["Le produit", "La composition", "Pièces jointes", "Résumé"]
const components = [ProductStep, CompositionStep, AttachmentStep, SummaryStep]
</script>
