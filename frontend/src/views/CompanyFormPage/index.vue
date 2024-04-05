<template>
  <div class="fr-container my-8 flex flex-col">
    <!-- Stepper -->
    <DsfrStepper :steps="steps" :currentStep="step" v-if="step > 0" />

    <!-- Page content -->
    <Introduction v-if="step == 0" />
    <KeepAlive>
      <component
        :is="components[step - 1]"
        @exist="changeStep(1, 'Reprise d\'entreprise', TakeOverCompany, nextStep)"
        @unexist="changeStep(1, 'Création d\'entreprise', CreateCompany, nextStep)"
      />
    </KeepAlive>

    <!-- Navigation buttons -->
    <div class="mt-4 md:mt-8 flex justify-center gap-x-4">
      <DsfrButton @click="nextStep" v-if="step == 0" label="Démarrer !" size="lg" />
      <DsfrButton @click="prevStep" v-if="step > 0" label="Étape précédente" icon="ri-arrow-left-line" tertiary />
      <!-- <DsfrButton
        @click="nextStep"
        v-if="step > 0 && step < steps.length"
        label="Étape suivante"
        icon="ri-arrow-right-line"
        iconRight
      /> -->
      <DsfrButton v-if="step == steps.length" label="C'est terminé !" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
// not considered as a step since not in the stepper
import Introduction from "./Introduction" // 0
// steps
import Identification from "./steps/Identification" // 1
import CreateCompany from "./steps/CreateCompany" // 2A
import TakeOverCompany from "./steps/TakeOverCompany" // 2B
import Summary from "./steps/Summary" // 3

const step = ref(0) // 0 shows Introduction component, outside of DSFRStepper
const prevStep = () => (step.value -= 1)
const nextStep = () => (step.value += 1)

// Steps and components follow the same step order, from 1 to N
const steps = ref(["Identification de l'entreprise", "Création ou reprise d'entreprise", "Récapitulatif"])
const components = [Identification, undefined, Summary] // NOTE: may need to be reactive at some point

// Steps are dynamic and can change according to events
const changeStep = (index, name, component, callback) => {
  steps.value[index] = name
  components[index] = component
  if (callback) callback()
}
</script>
