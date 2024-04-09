<template>
  <div class="fr-container my-8 flex flex-col">
    <!-- Stepper -->
    <DsfrStepper :steps="steps" :currentStep="step" v-if="step > 0" />

    <!-- Page content -->
    <Introduction v-if="step == 0" />
    <KeepAlive>
      <component :is="components[step - 1]" @changeStep="handleChangeStepEvent" />
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
      <DsfrButton label="Retour au tableau de bord" v-if="step > 0" tertiary icon="ri-arrow-go-back-fill" />
      <DsfrButton v-if="step == steps.length" label="C'est terminé !" />
    </div>
  </div>
</template>

<script setup>
import { ref, defineAsyncComponent } from "vue"
import { useCreateCompanyStore } from "@/stores/createCompany"
import Introduction from "./Introduction" // 0
import PickCountry from "./steps/PickCountry" // 1
import Summary from "./steps/Summary" // 4

const step = ref(0) // 0 shows Introduction component, outside of DSFRStepper
const prevStep = () => (step.value -= 1)
const nextStep = () => (step.value += 1)

// Steps and components follow the same step order, from 1 to N
const steps = ref([
  "Pays de l'entreprise",
  "Identification de l'entreprise",
  "Enregistrement ou reprise d'entreprise",
  "Récapitulatif",
])

// Les `undefined` correspondent à des étapes dynamiques, qui seront définies plus tard en fonction des réponses
const components = [PickCountry, undefined, undefined, Summary]

// Helper qui récupère le component d'une étape à partir de son nom
const stepComponentFromName = (name) => defineAsyncComponent(() => import(`./steps/${name}`))

// Helper pour changer le contenu d'une étape
const handleChangeStepEvent = (event) => {
  steps.value[event.index] = event.name
  components[event.index] = stepComponentFromName(event.component)
  if (event.goToNextStep) nextStep()
}

// Puisqu'un store est utilisé pour le process, on pense à le réinitialiser si la démarche (re)démarre
useCreateCompanyStore().resetCompany()

// WARN: casse la logique de précedent/suivant
// Sinon un bouton "annuler et recommencer" à la place ? Il y aurait plus le récapitulatif ?
// const removeStep = (index, callback) => {
//   steps.value.splice(index, 1)
//   if (callback) callback()
// }
</script>