<template>
  <div>
    <div class="bg-grey-975! p-6">
      <h2 id="pieces-jointes">Pièces jointes</h2>
      <CompactAttachmentGrid :attachments="declaration.attachments" />
      <h2 id="dernier-commentaire">Dernier commentaire</h2>
      <LastComment class="mb-6" :snapshot="lastSnapshot" />
      <h2 id="composition-produit">Composition produit</h2>
      <CompositionInfo :useAccordions="true" :showElementAuthorization="true" :model-value="declaration" />
      <div v-if="showComputedSubstances">
        <p class="font-bold mt-8">Substances contenues dans la composition :</p>
        <ComputedSubstancesInfo :model-value="declaration" />
      </div>
      <p class="font-bold mt-8" v-else>Pas de substances calculées à partir de la composition</p>
      <h2 id="resultat-instruction">Résultat de l'instruction</h2>
      <InstructionResults :model-value="declaration" />
    </div>
    <div class="p-6">
      <h2 id="notes">Notes à destination de l'administration</h2>
      <DsfrAlert small description="Ce segment est en construction" class="mb-6" />
    </div>
  </div>
</template>

<script setup>
import CompactAttachmentGrid from "@/components/CompactAttachmentGrid.vue"
import LastComment from "./LastComment"
import InstructionResults from "./InstructionResults"
import CompositionInfo from "@/components/CompositionInfo"
import ComputedSubstancesInfo from "@/components/ComputedSubstancesInfo"
import { computed } from "vue"

const props = defineProps({ declaration: Object, snapshots: Array })

const lastSnapshot = computed(() => props.snapshots?.findLast((x) => !!x.comment))

const showComputedSubstances = computed(() => {
  if (props.declaration?.computedSubstances?.length) return true
  return props.declaration.declaredPlants
    .concat(props.declaration.declaredMicroorganisms)
    .concat(props.declaration.declaredSubstances)
    .concat(props.declaration.declaredIngredients)
    .some((x) => x.requestStatus === "REPLACED" && x.element?.substances?.length)
})
</script>
