<template>
  <div>
    <SummaryInfoSegment v-if="!!payload.teleicareId" label="Identifiant Teleicare" :value="payload.teleicareId" />
    <SummaryInfoSegment label="Nom du produit" :value="payload.name" />
    <SummaryInfoSegment label="Marque" :value="payload.brand" />
    <SummaryInfoSegment label="Gamme" :value="payload.gamme" />
    <SummaryInfoSegment label="Description" :value="payload.description" />
    <SummaryInfoSegment label="Populations cibles" :value="populationNames" />
    <SummaryInfoSegment label="Populations à consommation déconseillée" :value="conditionNames" />
    <SummaryInfoSegment label="Mise en garde et avertissement" :value="payload.warning" />
    <SummaryInfoSegment label="Forme galénique" :value="galenicFormulationsNames" />
    <SummaryInfoSegment label="Mode d'emploi" :value="payload.instructions" />
    <SummaryInfoSegment label="Unité de consommation" :value="unitInfo" />
    <SummaryInfoSegment label="Dose journalière recommandée" :value="payload.dailyRecommendedDose" />
    <SummaryInfoSegment label="Conditionnement" :value="payload.conditioning" />
    <SummaryInfoSegment label="Durabilité minimale / DLUO (en mois)" :value="payload.minimumDuration" />
    <SummaryInfoSegment label="Objectifs / effets" :value="effectsNames" />
  </div>
</template>

<script setup>
import SummaryInfoSegment from "./SummaryInfoSegment"
import { getUnitQuantityString } from "@/utils/elements"
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"

const props = defineProps({ payload: Object })

const { units, populations, conditions, effects, galenicFormulations } = storeToRefs(useRootStore())
const unitInfo = computed(() => getUnitQuantityString(props.payload, units))

const galenicFormulationsNames = computed(() => {
  if (!props.payload.galenicFormulation) return null
  else if (props.payload.otherGalenicFormulation)
    return "Autre (à préciser) : ".concat(props.payload.otherGalenicFormulation)
  return galenicFormulations.value?.find((y) => y.id === parseInt(props.payload.galenicFormulation))?.name
})

const effectsNames = computed(() => {
  const findName = (id) => effects.value?.find((y) => y.id === id)?.name
  const allEffects = props.payload.otherEffects
    ? props.payload.effects.map(findName).concat("Autre (à préciser) : ".concat(props.payload.otherEffects))
    : props.payload.effects.map(findName)

  const indexOtherEffectLabel = allEffects.indexOf("Autre (à préciser)")
  if (indexOtherEffectLabel !== -1) {
    allEffects.splice(indexOtherEffectLabel, 1)
  }
  return allEffects.join(", ")
})

const populationNames = computed(() => {
  const findName = (id) => populations.value?.find((y) => y.id === id)?.name
  return props.payload.populations.map(findName).join(", ")
})
const conditionNames = computed(() => {
  const findName = (id) => conditions.value?.find((y) => y.id === id)?.name
  const allConditions = props.payload.otherConditions
    ? props.payload.conditionsNotRecommended
        .map(findName)
        .concat("Autre (à préciser) : ".concat(props.payload.otherConditions))
    : props.payload.conditionsNotRecommended.map(findName)

  const indexOtherConditionLabel = allConditions.indexOf("Autre (à préciser)")
  if (indexOtherConditionLabel !== -1) {
    allConditions.splice(indexOtherConditionLabel, 1)
  }
  return allConditions.join(", ")
})
</script>
