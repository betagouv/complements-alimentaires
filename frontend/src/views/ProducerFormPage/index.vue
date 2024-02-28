<template>
  <div class="bg-blue-france-975 border border-slate-300">
    <div class="fr-container pt-4 pb-6">
      <DsfrStepper class="!mb-0" :currentStep="currentStep" :steps="steps" />
    </div>
  </div>
  <div class="fr-container">
    <StepButtons
      class="mb-6 mt-3"
      @next="goForward"
      @previous="goBackward"
      :disablePrevious="disablePrevious"
      :disableNext="disableNext"
    />
    <component :is="components[currentStep - 1]" v-model="payload"></component>
    <StepButtons
      class="mb-3 mt-6"
      @next="goForward"
      @previous="goBackward"
      :disablePrevious="disablePrevious"
      :disableNext="disableNext"
    />
  </div>
</template>
<script setup>
import { onMounted, ref, computed, watch } from "vue"
import ProductStep from "./ProductStep"
import CompositionStep from "./CompositionStep"
import SummaryStep from "./SummaryStep"
import AttachmentStep from "./AttachmentStep"
import StepButtons from "./StepButtons"
import { useRoute, useRouter } from "vue-router"

const payload = ref({
  effects: [],
  targetConditions: [],
  targetPopulations: [],
  elements: [],
  substances: [],
})

const currentStep = ref(null)
const steps = ["Le produit", "La composition", "Pièces jointes", "Résumé"]
const components = [ProductStep, CompositionStep, AttachmentStep, SummaryStep]

const goForward = () => router.push({ query: { step: currentStep.value + 1 } })
const goBackward = () => router.push({ query: { step: currentStep.value - 1 } })

const disablePrevious = computed(() => currentStep.value === 1)
const disableNext = computed(() => currentStep.value === steps.length)

const route = useRoute()
const router = useRouter()

const ensureStepInUrl = () => {
  if (route.query.step && parseInt(route.query.step) >= 1 && parseInt(route.query.step) <= steps.length)
    currentStep.value = parseInt(route.query.step)
  else router.replace({ query: { step: 1 } })
}

onMounted(ensureStepInUrl)
watch(() => route.query.step, ensureStepInUrl)
</script>
