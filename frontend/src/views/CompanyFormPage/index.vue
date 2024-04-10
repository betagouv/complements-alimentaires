<template>
  <div class="fr-container my-8 flex flex-col">
    <!-- Stepper -->
    <DsfrStepper :steps="steps" :currentStep="step" v-if="step > 0" />

    <!-- Page content -->
    <Introduction v-if="step == 0" @changeStep="handleChangeStepEvent" />
    <KeepAlive>
      <component :is="components[step - 1]" @changeStep="handleChangeStepEvent" />
    </KeepAlive>

    <!-- Previous Navigation Button -->
    <DsfrButton
      v-if="step > 0 && step < steps.length"
      class="mt-4"
      @click="prevStep"
      iconOnly
      icon="ri-arrow-left-line"
      tertiary
      noOutline
      size="sm"
    />
  </div>
</template>

<script setup>
import { ref, defineAsyncComponent } from "vue"
import { useCreateCompanyStore } from "@/stores/createCompany"
import Introduction from "./Introduction" // 0
import PickCountry from "./steps/PickCountry" // 1

const step = ref(0) // 0 montre un composant en dehors du DSFRStepper

// Puisqu'un store est utilisé pendant le process, on pense à le réinitialiser quand la démarche (re)démarre
useCreateCompanyStore().resetCompany()

// Steps et components suivent le même ordre, de 1 à N
const steps = ref([
  "Pays de l'entreprise",
  "Identification de l'entreprise",
  "Enregistrement ou reprise d'entreprise",
  "Fin",
])

// Les `undefined` correspondent à des étapes dynamiques, qui seront définies plus tard en fonction des réponses
// Le fait de les inclure permet de montrer à l'utilisateur un nombre d'étapes prévues (ici, 4)
const components = [PickCountry, undefined, undefined, undefined]

// Helpers -----------------------------------------------------------------------------------------------------------

const prevStep = () => (step.value -= 1)
const nextStep = () => (step.value += 1)

// Récupère le component d'une étape à partir de son nom
const stepComponentFromName = (name) => defineAsyncComponent(() => import(`./steps/${name}`))

// Passe à la prochaine étape, en changeant (ou pas) son contenu (nom de l'étape et composant affiché dynamiquement)
const handleChangeStepEvent = (event) => {
  if (event && event.name) steps.value[step.value] = event.name
  if (event && event.component) components[step.value] = stepComponentFromName(event.component)
  nextStep()
}
</script>
