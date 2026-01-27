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
    <div class="flex items-center section-header">
      <h3 class="fr-h6 mb-0">Informations sur le produit</h3>
      <SummaryModificationButton class="ml-4" v-if="!readonly" :to="editLink(0)" tabName="produit" />
    </div>
    <ProductInfoSegment :payload="payload" />
    <div>
      <div class="flex items-center mt-8! section-header">
        <h3 class="fr-h6 mb-0">Composition</h3>
        <SummaryModificationButton class="ml-4" v-if="!readonly" :to="editLink(1)" tabName="composition" />
      </div>

      <CompositionInfo
        v-model="payload"
        :useAccordions="useAccordions"
        :showElementAuthorization="showElementAuthorization"
      />

      <ComputedSubstancesInfo v-model="payload" tableTitle="Substances contenues dans la composition" class="mt-8" />

      <div class="flex items-center mt-8! section-header">
        <h3 class="fr-h6 mb-0">Adresse sur l'étiquetage</h3>
        <SummaryModificationButton
          class="ml-4"
          v-if="!readonly"
          :to="editLink(0)"
          tabName="produit"
          suffix="l'adresse"
        />
      </div>
      <AddressLine :payload="payload" />
      <div class="flex items-center mt-8! section-header">
        <h3 class="fr-h6 mb-0">Pièces jointes</h3>
        <SummaryModificationButton class="ml-4" v-if="!readonly" :to="attachmentLink" tabName="Pièces jointes" />
      </div>
      <RequiresAnalysisReportNotice :declaration="payload" class="mb-4" />
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
</template>

<script>
export default { name: "DeclarationSummary" }
</script>

<script setup>
import { computed } from "vue"
import AddressLine from "@/components/AddressLine"
import ProductInfoSegment from "@/components/ProductInfoSegment"
import ArticleInfoRow from "./ArticleInfoRow"
import CompositionInfo from "@/components/CompositionInfo"
import ComputedSubstancesInfo from "@/components/ComputedSubstancesInfo"
import FilePreview from "@/components/FilePreview"
import { useRouter } from "vue-router"
import SummaryModificationButton from "./SummaryModificationButton"
import HistoryBadge from "../History/HistoryBadge.vue"
import RequiresAnalysisReportNotice from "@/components/RequiresAnalysisReportNotice"
import { hasNewElements } from "@/utils/elements"

const router = useRouter()

const payload = defineModel()
defineProps({
  readonly: Boolean,
  allowArticleChange: Boolean,
  useAccordions: Boolean,
  showElementAuthorization: Boolean,
})

const editLink = (tab) => ({ query: { tab } })

const attachmentLink = computed(() => {
  return hasNewElements(payload.value) ? editLink(3) : editLink(2)
})
</script>

<style scoped>
@reference "../../styles/index.css";

.section-header {
  @apply border p-2 sm:p-4 bg-blue-france-975 mb-6;
}
</style>
