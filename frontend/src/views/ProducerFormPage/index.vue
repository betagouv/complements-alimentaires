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
import { useRootStore } from "@/stores/root"
import { onMounted, ref, computed, watch } from "vue"
import ProductStep from "./ProductStep"
import CompositionStep from "./CompositionStep"
import SummaryStep from "./SummaryStep"
import AttachmentStep from "./AttachmentStep"
import NewElementStep from "./NewElementStep"
import StepButtons from "./StepButtons"
import { useRoute, useRouter } from "vue-router"

const store = useRootStore()
store.fetchConditions()
store.fetchPopulations()
store.fetchPlantParts()
store.fetchUnits()

const payload = ref({
  effects: [],
  conditionsNotRecommended: [],
  populations: [],
  elements: [],
  substances: [],
  files: {
    labels: [],
    others: [],
  },
  labelAddress: {},
})

const hasNewElements = computed(() => payload.value.elements.some((x) => x.element.new))

const currentStep = ref(null)
const steps = computed(() => {
  const baseSteps = ["Le produit", "La composition", "Pièces jointes", "Résumé"]
  if (hasNewElements.value) baseSteps.splice(2, 0, "Nouveaux éléments")
  return baseSteps
})

const components = computed(() => {
  const baseComponents = [ProductStep, CompositionStep, AttachmentStep, SummaryStep]
  if (hasNewElements.value) baseComponents.splice(2, 0, NewElementStep)
  return baseComponents
})

const goForward = () => router.push({ query: { step: currentStep.value + 1 } })
const goBackward = () => router.push({ query: { step: currentStep.value - 1 } })

const disablePrevious = computed(() => currentStep.value === 1)
const disableNext = computed(() => currentStep.value === steps.value.length)

const route = useRoute()
const router = useRouter()

const ensureStepInUrl = () => {
  if (route.query.step && parseInt(route.query.step) >= 1 && parseInt(route.query.step) <= steps.value.length)
    currentStep.value = parseInt(route.query.step)
  else router.replace({ query: { step: 1 } })
}

onMounted(ensureStepInUrl)
watch(() => route.query.step, ensureStepInUrl)
</script>
