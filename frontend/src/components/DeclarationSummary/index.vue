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
      <h3 class="fr-h6 mt-8!">
        Pièces jointes
        <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(2))" />
      </h3>
      <CompactAttachmentGrid :attachments="payload.attachments" />
    </div>
    <h3 class="fr-h6">
      Informations sur le produit
      <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(0))" />
    </h3>
    <ProductInfoSegment :payload="payload" />
    <div>
      <h3 class="fr-h6 mt-8!">
        Composition
        <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(1))" />
      </h3>

      <CompositionInfo
        v-model="payload"
        :useAccordions="useAccordions"
        :showElementAuthorization="showElementAuthorization"
      />

      <p class="font-bold mt-8" v-if="payload.computedSubstances.length">Substances contenues dans la composition :</p>
      <ComputedSubstancesInfo v-model="payload" />

      <div v-if="!payload.siccrfId">
        <h3 class="fr-h6 mt-8!">
          Adresse sur l'étiquetage
          <SummaryModificationButton class="ml-4" v-if="!readonly" @click="router.push(editLink(1))" />
        </h3>
        <AddressLine :payload="payload" />
      </div>
      <div v-if="!useCompactAttachmentView & !payload.siccrfId">
        <h3 class="fr-h6 mt-8!">
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
import AddressLine from "@/components/AddressLine"
import ProductInfoSegment from "@/components/ProductInfoSegment"
import ArticleInfoRow from "./ArticleInfoRow"
import CompositionInfo from "@/components/CompositionInfo"
import ComputedSubstancesInfo from "@/components/ComputedSubstancesInfo"
import FilePreview from "@/components/FilePreview"
import { useRouter } from "vue-router"
import SummaryModificationButton from "./SummaryModificationButton"
import HistoryBadge from "../History/HistoryBadge.vue"
import CompactAttachmentGrid from "@/components/CompactAttachmentGrid"

const router = useRouter()

const payload = defineModel()
defineProps({
  readonly: Boolean,
  allowArticleChange: Boolean,
  useAccordions: Boolean,
  showElementAuthorization: Boolean,
  useCompactAttachmentView: Boolean,
})

const editLink = (tab) => ({ query: { tab } })
</script>

<style scoped>
@reference "../../styles/index.css";

h3 {
  @apply border p-2 sm:p-4 bg-blue-france-975;
}
</style>
