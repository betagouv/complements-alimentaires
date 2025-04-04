<template>
  <div>
    <HistoryBadge v-if="!!payload.siccrfId" class="mb-2" />
    <ArticleInfoRow
      v-model="payload"
      :hideArticle15Subtypes="!allowArticleChange"
      :allowChange="allowArticleChange"
      v-if="allowArticleChange || payload.article"
      class="mb-2"
    />
    <div v-if="useCompactAttachmentView">
      <h3 class="fr-h6 !mt-8">
        Pièces jointes
        <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(2))" />
      </h3>
      <div class="grid grid-cols-12 gap-3 mb-8">
        <div
          class="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-3 overflow-auto"
          v-for="(file, index) in payload.attachments"
          :key="`file-download-${index}`"
        >
          <DsfrFileDownload
            :title="`${truncateMiddle(file.name, 22)}`"
            :href="file.file"
            :size="file.size"
            :format="file.typeDisplay"
            :download="null"
            target="_blank"
          />
        </div>
      </div>
    </div>
    <h3 class="fr-h6">
      Informations sur le produit
      <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(0))" />
    </h3>
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
    <div>
      <h3 class="fr-h6 !mt-8">
        Composition
        <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(1))" />
      </h3>

      <SummaryElementList
        :useAccordions="useAccordions"
        :showElementAuthorization="showElementAuthorization"
        objectType="plant"
        :elements="payload.declaredPlants"
      />
      <SummaryElementList
        :useAccordions="useAccordions"
        :showElementAuthorization="showElementAuthorization"
        objectType="microorganism"
        :elements="payload.declaredMicroorganisms"
      />
      <SummaryElementList
        objectType="form_of_supply"
        :useAccordions="useAccordions"
        :showElementAuthorization="showElementAuthorization"
        :elements="getObjectSubTypeList(payload.declaredIngredients, 'form_of_supply')"
      />
      <SummaryElementList
        :useAccordions="useAccordions"
        :showElementAuthorization="showElementAuthorization"
        objectType="aroma"
        :elements="getObjectSubTypeList(payload.declaredIngredients, 'aroma')"
      />
      <SummaryElementList
        objectType="additive"
        :useAccordions="useAccordions"
        :showElementAuthorization="showElementAuthorization"
        :elements="getObjectSubTypeList(payload.declaredIngredients, 'additive')"
      />
      <SummaryElementList
        objectType="active_ingredient"
        :useAccordions="useAccordions"
        :showElementAuthorization="showElementAuthorization"
        :elements="getObjectSubTypeList(payload.declaredIngredients, 'active_ingredient')"
      />
      <SummaryElementList
        objectType="non_active_ingredient"
        :useAccordions="useAccordions"
        :showElementAuthorization="showElementAuthorization"
        :elements="getObjectSubTypeList(payload.declaredIngredients, 'non_active_ingredient')"
      />
      <SummaryElementList
        objectType="substance"
        :useAccordions="useAccordions"
        :showElementAuthorization="showElementAuthorization"
        :elements="payload.declaredSubstances"
      />

      <p class="font-bold mt-8" v-if="payload.computedSubstances.length">Substances contenues dans la composition :</p>
      <DsfrAlert
        v-if="replacedRequestsWithSubstances.length"
        type="warning"
        class="mb-4"
        title="Vérifiez les doses totales des substances"
      >
        <p>
          Les ingrédients suivants, ajoutés pour remplacer une demande, rajoutent des substances dans la composition.
        </p>
        <p>
          Veuillez vérifier que les doses totales des substances restent pertinentes. Si besoin, renvoyez la déclaration
          vers le déclarant pour les mettre à jour.
        </p>
        <ul>
          <li v-for="i in replacedRequestsWithSubstances" :key="`${i.type}-${i.id}`">
            {{ i.element.name }}
          </li>
        </ul>
      </DsfrAlert>
      <SubstancesTable v-model="payload" readonly />
      <div v-if="!payload.siccrfId">
        <h3 class="fr-h6 !mt-8">
          Adresse sur l'étiquetage
          <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(1))" />
        </h3>
        <AddressLine :payload="payload" />
      </div>
      <div v-if="!useCompactAttachmentView & !payload.siccrfId">
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
    </div>
  </div>
</template>

<script>
export default { name: "DeclarationSummary" }
</script>

<script setup>
import { getObjectSubTypeList, getUnitQuantityString } from "@/utils/elements"
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
import HistoryBadge from "../History/HistoryBadge.vue"
import { truncateMiddle } from "@/utils/string"

const router = useRouter()
const { units, populations, conditions, effects, galenicFormulations } = storeToRefs(useRootStore())

const payload = defineModel()
defineProps({
  readonly: Boolean,
  allowArticleChange: Boolean,
  useAccordions: Boolean,
  showElementAuthorization: Boolean,
  useCompactAttachmentView: Boolean,
})
const unitInfo = computed(() => getUnitQuantityString(payload.value, units))

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

const replacedRequestsWithSubstances = computed(() => {
  const data = payload.value
  if (!data) return false
  const elements = data.declaredPlants
    .concat(data.declaredMicroorganisms)
    .concat(data.declaredSubstances)
    .concat(data.declaredIngredients)
  return elements?.filter((i) => i.requestStatus === "REPLACED" && i.element?.substances?.length)
})
</script>

<style scoped>
h3 {
  @apply border p-2 sm:p-4 bg-blue-france-975;
}
</style>
