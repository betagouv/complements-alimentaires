<template>
  <div class="fr-container mb-8 flex flex-col">
    <!-- Stepper -->
    <DsfrStepper :steps="mapping.map((x) => x.name)" :currentStep="step" />

    <!-- Contenu dynamique - le KeepAlive permet de garder le contenu des réponses en naviguant -->
    <KeepAlive>
      <component
        :is="stepComponentFromName(mapping.map((x) => x.component)[step - 1])"
        @changeStep="handleChangeStepEvent"
        v-model="company"
      />
    </KeepAlive>

    <!-- Bouton de retour en arrière - non affiché à la 1ère et la dernière étape qui correspond à la confirmation -->
    <DsfrButton
      v-if="step > 1 && step < mapping.length"
      class="mt-4"
      @click="step -= 1"
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

const step = ref(1)

// Cet object agit comme un store disponible au sein de tous les différents composants qui affichent les étapes
const company = ref({})

// Mapping entre le nom des étapes (utilisé par le DsfrStepper) et leur component associé.
// L'index est déterminé par la position dans l'array.
// Le nom/composant des étapes peuvent changer en cours de route en fonction des réponses.
// Les `undefined` seront changés en cours de route.
const mapping = ref([
  { name: "Créer ou rejoindre une entreprise", component: "Introduction" },
  { name: "Pays de l'entreprise", component: "PickCountry" },
  { name: "Identification de l'entreprise", component: undefined },
  { name: "Enregistrement ou reprise d'entreprise", component: undefined },
  { name: "Fin", component: undefined },
])

// Helpers -----------------------------------------------------------------------------------------------------------

// Récupère un component à partir de son nom
const stepComponentFromName = (name) => defineAsyncComponent(() => import(`./${name}`))

// Passe à la prochaine étape, en changeant (ou pas) son contenu (nom de l'étape et/ou composant affiché dynamiquement)
const handleChangeStepEvent = (event) => {
  if (event && event.name) mapping.value[step.value].name = event.name
  if (event && event.component) mapping.value[step.value].component = event.component

  step.value += 1
  if (event && event.deleteStepAfter) {
    // supprime l'étape d'après totalement - attention, ne doit être utilisé que pour une étape de confirmation.
    // car si le retour en arrière est en encore possible, alors l'étape supprimée ne reviendrait pas.
    mapping.value.splice(step.value, 1)
  }
}
</script>
