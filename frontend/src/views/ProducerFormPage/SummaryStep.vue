<template>
  <h2 class="fr-h6">
    <v-icon class="mr-1" name="ri-file-text-line" />
    Votre démarche
  </h2>

  <h3 class="fr-h6">
    Informations sur le produit
    <router-link class="fr-btn fr-btn--secondary fr-btn--sm ml-4" :to="editLink(1)">Modifier</router-link>
  </h3>
  <div>
    <SummaryInfoSegment label="Nom du produit" :value="payload.name" />
    <SummaryInfoSegment label="Marque" :value="payload.brand" />
    <SummaryInfoSegment label="Gamme" :value="payload.gamme" />
    <SummaryInfoSegment label="Arôme" :value="payload.flavor" />
    <SummaryInfoSegment label="Description" :value="payload.description" />
    <SummaryInfoSegment label="Forme galénique" :value="payload.galenicFormulation" />
    <SummaryInfoSegment label="Unité de consommation" :value="unitInfo" />
    <SummaryInfoSegment label="Conditionnements" :value="payload.conditioning" />
    <SummaryInfoSegment label="Dose journalière recommandée" :value="payload.dailyRecommendedDose" />
    <SummaryInfoSegment label="Durabilité minimale / DLUO (en mois)" :value="payload.minimumDuration" />
    <SummaryInfoSegment label="Mode d'emploi" :value="payload.instructions" />
    <SummaryInfoSegment label="Mise en garde et avertissement" :value="payload.warnings" />
    <SummaryInfoSegment label="Populations cible" :value="populationNames" />
    <SummaryInfoSegment label="Consommation déconseillée" :value="conditionNames" />
    <SummaryInfoSegment label="Objectifs / effets" :value="effects" />
  </div>

  <h3 class="fr-h6 !mt-8">
    Composition
    <router-link class="fr-btn fr-btn--secondary fr-btn--sm ml-4" :to="editLink(2)">Modifier</router-link>
  </h3>
  <template v-if="payload.elements.length">
    <ul>
      <SummaryElementItem
        class="mb-2 last:mb-0"
        v-for="(element, index) in payload.elements"
        :key="`element-${index}`"
        :element="element"
      />
    </ul>

    <h4 class="fr-text--md !mt-6">Détail sur les substances actives :</h4>
    <SubstancesTable v-model="payload" readonly />
  </template>

  <h3 class="fr-h6 !mt-8">
    Pièces jointes
    <router-link class="fr-btn fr-btn--secondary fr-btn--sm ml-4" :to="editLink(3)">Modifier</router-link>
  </h3>
  <div class="grid grid-cols-12 gap-3">
    <FilePreview
      class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3"
      v-for="(file, index) in files"
      :key="`file-${index}`"
      :file="file"
      readonly
    />
  </div>
</template>

<script setup>
import { computed } from "vue"
import SummaryInfoSegment from "./SummaryInfoSegment"
import SummaryElementItem from "./SummaryElementItem"
import SubstancesTable from "./SubstancesTable"
import FilePreview from "./FilePreview"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"

const { populations, conditions } = storeToRefs(useRootStore())

const payload = defineModel()
const unitInfo = computed(() => {
  if (!payload.value.unitQuantity) return null
  return `${payload.value.unitQuantity} ${payload.value.unitMeasurement || "-"}`
})
const effects = computed(() => {
  const otherEffects = payload.value.otherEffects
  const allEffects = otherEffects ? payload.value.effects.concat([otherEffects]) : payload.value.effects
  return allEffects.join(", ")
})
const files = computed(() => {
  const labelFiles = payload.value.files.labels
  const otherFiles = payload.value.files.others
  return labelFiles.concat(otherFiles)
})
const populationNames = computed(() => {
  const findName = (id) => populations.value.find((y) => y.id === id)?.name
  return payload.value.populations.map(findName).join(", ")
})
const conditionNames = computed(() => {
  const findName = (id) => conditions.value.find((y) => y.id === id)?.name
  return payload.value.conditionsNotRecommended.map(findName).join(", ")
})

const editLink = (step) => ({ name: "ProducerFormPage", query: { step } })
</script>

<style scoped>
h3 {
  @apply border p-2 sm:p-4 bg-blue-france-975;
}
</style>
