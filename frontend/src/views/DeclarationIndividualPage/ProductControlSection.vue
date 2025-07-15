<template>
  <div class="p-6">
    <SectionHeader id="resume" icon="ri-ball-pen-fill" text="Résumé de l'instruction" />
    <InfoTable class="mb-8" :items="summaryItems" />
    <SectionHeader id="vue-ensemble" icon="ri-eye-line" text="Vue d'ensemble" />
    <ProductInfoSegment class="mb-8" :payload="declaration" />
    <SectionHeader id="composition-produit" icon="ri-capsule-fill" text="Composition produit" />
    <CompositionInfo :useAccordions="true" :showElementAuthorization="true" :model-value="declaration" />
    <div v-if="showComputedSubstances">
      <p class="font-bold mt-8">Substances contenues dans la composition :</p>
      <ComputedSubstancesInfo :model-value="declaration" />
    </div>
    <p class="font-bold mt-8" v-else>Pas de substances calculées à partir de la composition</p>

    <SectionHeader id="pieces-jointes" icon="ri-attachment-fill" text="Pièces jointes" />
    <CompactAttachmentGrid :attachments="declaration.attachments" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { isoToPrettyDate } from "@/utils/date"
import SectionHeader from "@/components/NewBepiasViews/SectionHeader"
import CompositionInfo from "@/components/CompositionInfo"
import CompactAttachmentGrid from "@/components/CompactAttachmentGrid"
import ComputedSubstancesInfo from "@/components/ComputedSubstancesInfo"
import ProductInfoSegment from "@/components/ProductInfoSegment"
import InfoTable from "@/components/InfoTable.vue"

const props = defineProps({ declaration: Object, snapshots: Array })

const showComputedSubstances = computed(() => {
  if (props.declaration?.computedSubstances?.length) return true
  return props.declaration.declaredPlants
    .concat(props.declaration.declaredMicroorganisms)
    .concat(props.declaration.declaredSubstances)
    .concat(props.declaration.declaredIngredients)
    .some((x) => x.requestStatus === "REPLACED" && x.element?.substances?.length)
})

const summaryItems = computed(() => {
  const d = props.declaration
  if (!d) return []
  return [
    { title: "No. de déclartion", body: [d.id || d.siccrfId || d.teleicareDeclarationNumber] },
    { title: "Statut du produit", body: [d.simplifiedStatus] },
    {
      title: "Date d'application du statut",
      body: [d.simplifiedStatusDate ? isoToPrettyDate(d.simplifiedStatusDate) : ""],
    },
  ]
})
</script>
