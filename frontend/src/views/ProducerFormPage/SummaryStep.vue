<template>
  <DsfrAlert class="mb-8">
    <p class="mb-2">Vous pouvez sauvegarder cette démarche pour la reprendre plus tard</p>
    <DsfrButton @click="saveDraft" label="Sauvegarder en tant que brouillon" />
  </DsfrAlert>

  <SectionTitle title="Votre démarche" sizeTag="h6" icon="ri-file-text-line" />

  <h3 class="fr-h6">
    Informations sur le produit
    <DsfrButton secondary class="ml-4" label="Modifier" size="small" @click="router.push(editLink(1))" />
  </h3>
  <div>
    <SummaryInfoSegment label="Nom du produit" :value="payload.name" />
    <SummaryInfoSegment label="Marque" :value="payload.brand" />
    <SummaryInfoSegment label="Gamme" :value="payload.gamme" />
    <SummaryInfoSegment label="Arôme" :value="payload.flavor" />
    <SummaryInfoSegment label="Description" :value="payload.description" />
    <SummaryInfoSegment label="Forme galénique" :value="galenicFormulationsNames" />
    <SummaryInfoSegment label="Unité de consommation" :value="unitInfo" />
    <SummaryInfoSegment label="Conditionnements" :value="payload.conditioning" />
    <SummaryInfoSegment label="Dose journalière recommandée" :value="payload.dailyRecommendedDose" />
    <SummaryInfoSegment label="Durabilité minimale / DLUO (en mois)" :value="payload.minimumDuration" />
    <SummaryInfoSegment label="Mode d'emploi" :value="payload.instructions" />
    <SummaryInfoSegment label="Mise en garde et avertissement" :value="payload.warnings" />
    <SummaryInfoSegment label="Populations cible" :value="populationNames" />
    <SummaryInfoSegment label="Consommation déconseillée" :value="conditionNames" />
    <SummaryInfoSegment label="Objectifs / effets" :value="effectsNames" />
  </div>

  <h3 class="fr-h6 !mt-8">
    Composition
    <DsfrButton secondary class="ml-4" label="Modifier" size="small" @click="router.push(editLink(2))" />
  </h3>

  <SummaryElementList objectType="plant" :elements="payload.declaredPlants" />
  <SummaryElementList objectType="microorganism" :elements="payload.declaredMicroorganisms" />
  <SummaryElementList objectType="ingredient" :elements="payload.declaredIngredients" />
  <SummaryElementList objectType="substance" :elements="payload.declaredSubstances" />

  <SubstancesTable v-model="payload" readonly />

  <h3 class="fr-h6 !mt-8">
    Pièces jointes
    <DsfrButton secondary class="ml-4" label="Modifier" size="small" @click="router.push(editLink(3))" />
  </h3>
  <div class="grid grid-cols-12 gap-3">
    <FilePreview
      class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3"
      v-for="(file, index) in payload.attachments"
      :key="`file-${index}`"
      :file="file"
      readonly
    />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import SummaryInfoSegment from "./SummaryInfoSegment"
import SummaryElementList from "./SummaryElementList"
import SubstancesTable from "./SubstancesTable"
import FilePreview from "./FilePreview"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import useToaster from "@/composables/use-toaster"
import SectionTitle from "@/components/SectionTitle"

const router = useRouter()
const { populations, conditions, effects, galenicFormulation } = storeToRefs(useRootStore())

const payload = defineModel()
const unitInfo = computed(() => {
  if (!payload.value.unitQuantity) return null
  return `${payload.value.unitQuantity} ${payload.value.unitMeasurement || "-"}`
})

const galenicFormulationsNames = computed(() => {
  if (!payload.value.galenicFormulation) return null
  return galenicFormulation.value.find((y) => y.id === parseInt(payload.value.galenicFormulation))?.name
})

const effectsNames = computed(() => {
  const findName = (id) => effects.value.find((y) => y.id === id)?.name
  const otherEffects = payload.value.otherEffects
  const allEffects = otherEffects
    ? payload.value.effects.map(findName).concat("Autre (à préciser) : ".concat(otherEffects))
    : payload.value.effects.map(findName)

  const indexOtherEffectLabel = allEffects.indexOf("Autre (à préciser)")
  if (indexOtherEffectLabel !== -1) {
    allEffects.splice(indexOtherEffectLabel, 1)
  }
  return allEffects.join(", ")
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

const saveDraft = async () => {
  const isNewDeclaration = !payload.value.id
  const url = isNewDeclaration ? "/api/v1/declarations/" : `/api/v1/declarations/${payload.value.id}`
  const httpMethod = isNewDeclaration ? "post" : "put"
  const { response } = await useFetch(url, { headers: headers() })[httpMethod](payload)
  if (response.value.ok) {
    await router.replace({ name: "DeclarationsHomePage" })
    useToaster().addSuccessMessage("Votre démarche a été sauvegardée")
  } else {
    console.log(response)
  }
}
</script>

<style scoped>
h3 {
  @apply border p-2 sm:p-4 bg-blue-france-975;
}
</style>
