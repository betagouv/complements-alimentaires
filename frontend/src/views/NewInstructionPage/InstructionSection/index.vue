<template>
  <div>
    <div class="bg-grey-975! p-6">
      <ArticleInfoRow :modelValue="declaration" :allowChange="true" class="mb-4" />

      <SectionHeader id="pieces-jointes" icon="ri-attachment-fill" text="Pièces jointes" />
      <CompactAttachmentGrid :attachments="declaration.attachments" />

      <SectionHeader id="dernier-commentaire" icon="ri-chat-2-fill" text="Dernier commentaire" />
      <LastComment class="mb-6" :snapshot="lastSnapshot" />

      <SectionHeader id="composition-produit" icon="ri-capsule-fill" text="Composition produit" />
      <CompositionInfo :useAccordions="true" :showElementAuthorization="true" :model-value="declaration" />
      <div v-if="showComputedSubstances">
        <p class="font-bold mt-8">Substances contenues dans la composition :</p>
        <ComputedSubstancesInfo :model-value="declaration" />
      </div>
      <p class="font-bold mt-8" v-else>Pas de substances calculées à partir de la composition</p>

      <SectionHeader id="resultat-instruction" icon="ri-todo-fill" text="Résultat de l'instruction" />
      <InstructionResults :model-value="declaration" :readonly="!canInstruct" />
    </div>
    <div class="p-6">
      <SectionHeader id="notes" icon="ri-ball-pen-fill" text="Notes à destination de l'administration" />
      <AdministrationNotes v-if="!declaration.siccrfId" :model-value="declaration" :disableVisaNotes="true" />
      <p v-else>Déclaration importée depuis Téléicare, les commentaires ne sont pas disponibles.</p>
    </div>
  </div>
</template>

<script setup>
import CompactAttachmentGrid from "@/components/CompactAttachmentGrid.vue"
import LastComment from "./LastComment"
import InstructionResults from "./InstructionResults"
import CompositionInfo from "@/components/CompositionInfo"
import ComputedSubstancesInfo from "@/components/ComputedSubstancesInfo"
import AdministrationNotes from "@/components/AdministrationNotes"
import SectionHeader from "../SectionHeader"
import ArticleInfoRow from "@/components/DeclarationSummary/ArticleInfoRow"
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

const canInstruct = computed(() => props.declaration?.status === "ONGOING_INSTRUCTION")
</script>
