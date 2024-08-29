<template>
  <div>
    <ArticleInfoRow v-model="payload" v-if="showArticle" class="mb-2" />
    <h3 class="fr-h6">
      Informations sur le produit
      <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(0))" />
    </h3>
    <div>
      <SummaryInfoSegment label="Nom du produit" :value="payload.name" />
      <SummaryInfoSegment label="Marque" :value="payload.brand" />
      <SummaryInfoSegment label="Gamme" :value="payload.gamme" />
      <SummaryInfoSegment label="Description" :value="payload.description" />
      <SummaryInfoSegment label="Populations cibles" :value="populationNames" />
      <SummaryInfoSegment label="Populations à consommation déconseillée" :value="conditionNames" />
      <SummaryInfoSegment label="Forme galénique" :value="galenicFormulationsNames" />
      <SummaryInfoSegment label="Mode d'emploi" :value="payload.instructions" />
      <SummaryInfoSegment label="Unité de consommation" :value="unitInfo" />
      <SummaryInfoSegment label="Dose journalière recommandée" :value="payload.dailyRecommendedDose" />
      <SummaryInfoSegment label="Conditionnement" :value="payload.conditioning" />
      <SummaryInfoSegment label="Durabilité minimale / DLUO (en mois)" :value="payload.minimumDuration" />
      <SummaryInfoSegment label="Mise en garde et avertissement" :value="payload.warnings" />
      <SummaryInfoSegment label="Objectifs / effets" :value="effectsNames" />
    </div>

    <h3 class="fr-h6 !mt-8">
      Composition
      <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(1))" />
    </h3>

    <SummaryElementList objectType="plant" :elements="payload.declaredPlants" />
    <SummaryElementList objectType="microorganism" :elements="payload.declaredMicroorganisms" />
    <SummaryElementList
      objectType="form_of_supply"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'form_of_supply')"
    />
    <SummaryElementList objectType="aroma" :elements="getObjectSubTypeList(payload.declaredIngredients, 'aroma')" />
    <SummaryElementList
      objectType="additive"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'additive')"
    />
    <SummaryElementList
      objectType="active_ingredient"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'active_ingredient')"
    />
    <SummaryElementList
      objectType="non_active_ingredient"
      :elements="getObjectSubTypeList(payload.declaredIngredients, 'non_active_ingredient')"
    />
    <SummaryElementList objectType="substance" :elements="payload.declaredSubstances" />

    <p class="font-bold mt-8">Substances contenues dans la composition :</p>
    <SubstancesTable v-model="payload" readonly />

    <h3 class="fr-h6 !mt-8">
      Adresse sur l'étiquetage
      <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(1))" />
    </h3>
    <AddressLine :payload="payload" />

    <h3 class="fr-h6 !mt-8">
      Pièces jointes
      <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(2))" />
    </h3>
    <div class="grid grid-cols-12 gap-3 mb-8">
      <FilePreview
        class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3"
        v-for="(file, index) in payload.attachments"
        :key="`file-${index}`"
        :file="file"
        readonly
      />
    </div>
  </div>
</template>

<script>
export default { name: "DeclarationSummary" }
</script>

<script setup>
import { getObjectSubTypeList } from "@/utils/elements"
import { computed } from "vue"
import AddressLine from "@/components/AddressLine"
import SummaryInfoSegment from "./SummaryInfoSegment"
import SummaryElementList from "./SummaryElementList"
import ArticleInfoRow from "./ArticleInfoRow"
import SubstancesTable from "@/components/SubstancesTable"
import FilePreview from "@/components/FilePreview"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import SummaryModificationButton from "./SummaryModificationButton"

const router = useRouter()
const { units, populations, conditions, effects, galenicFormulations } = storeToRefs(useRootStore())

const payload = defineModel()
defineProps({ readonly: Boolean, showArticle: Boolean })
const unitInfo = computed(() => {
  if (!payload.value.unitQuantity) return null
  const unitMeasurement = units.value?.find?.((x) => x.id === payload.value.unitMeasurement)?.name || "-"
  return `${payload.value.unitQuantity} ${unitMeasurement}`
})

const galenicFormulationsNames = computed(() => {
  if (!payload.value.galenicFormulation) return null
  else if (payload.value.otherGalenicFormulation)
    return "Autre (à préciser) : ".concat(payload.value.otherGalenicFormulation)
  return galenicFormulations.value?.find((y) => y.id === parseInt(payload.value.galenicFormulation))?.name
})

const effectsNames = computed(() => {
  const findName = (id) => effects.value?.find((y) => y.id === id)?.name
  const allEffects = payload.value.otherEffects
    ? payload.value.effects.map(findName).concat("Autre (à préciser) : ".concat(payload.value.otherEffects))
    : payload.value.effects.map(findName)

  const indexOtherEffectLabel = allEffects.indexOf("Autre (à préciser)")
  if (indexOtherEffectLabel !== -1) {
    allEffects.splice(indexOtherEffectLabel, 1)
  }
  return allEffects.join(", ")
})

const populationNames = computed(() => {
  const findName = (id) => populations.value?.find((y) => y.id === id)?.name
  return payload.value.populations.map(findName).join(", ")
})
const conditionNames = computed(() => {
  const findName = (id) => conditions.value?.find((y) => y.id === id)?.name
  const allConditions = payload.value.otherConditions
    ? payload.value.conditionsNotRecommended
        .map(findName)
        .concat("Autre (à préciser) : ".concat(payload.value.otherConditions))
    : payload.value.conditionsNotRecommended.map(findName)

  const indexOtherConditionLabel = allConditions.indexOf("Autre (à préciser)")
  if (indexOtherConditionLabel !== -1) {
    allConditions.splice(indexOtherConditionLabel, 1)
  }
  return allConditions.join(", ")
})

const editLink = (tab) => ({ query: { tab } })
</script>

<style scoped>
h3 {
  @apply border p-2 sm:p-4 bg-blue-france-975;
}
</style>
