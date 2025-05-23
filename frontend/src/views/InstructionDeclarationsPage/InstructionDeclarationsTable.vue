<template>
  <DsfrTable
    ref="table"
    class="w-full"
    title="Toutes les déclarations"
    :headers="headers"
    :rows="rows"
    :no-caption="true"
    :pagination="false"
  />
</template>

<script setup>
import { computed } from "vue"
import { isoToPrettyDate } from "@/utils/date"
import { getStatusTagForCell } from "@/utils/components"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { articleOptionsWith15Subtypes } from "@/utils/mappings"
import CompanyTableCell from "@/components/CompanyTableCell"
import CircleIndicators from "./CircleIndicators"
import DeclarationName from "@/components/DeclarationName"

const { loggedUser } = storeToRefs(useRootStore())

const props = defineProps({ data: { type: Object, default: () => {} } })

const headers = ["", "ID", "Nom du produit", "Entreprise", "État", "Date limite de réponse", "Instruit par", "Article"]
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowAttrs: { class: needsAttention(x) ? "font-bold" : "" },
    rowData: [
      {
        component: CircleIndicators,
        declaration: x,
      },
      x.siccrfId ? (x.teleicareId ? x.teleicareId : "") : x.id,
      {
        component: DeclarationName,
        withHistoryBadge: !!x.siccrfId,
        text: x.name,
        to: { name: "InstructionPage", params: { declarationId: x.id } },
      },
      {
        component: CompanyTableCell,
        company: x.company?.socialName,
        mandatedCompany: x.mandatedCompany?.socialName,
      },
      getStatusTagForCell(x.status),
      x.responseLimitDate && isoToPrettyDate(x.responseLimitDate),
      x.instructor
        ? `${x.instructor.firstName} ${x.instructor.lastName}`
        : { component: "span", text: "Non-assigné", class: "italic" },
      x.article ? articleOptionsWith15Subtypes.find((y) => y.value === x.article)?.shortText : "",
    ],
  }))
)

const needsAttention = (declaration) =>
  !!declaration.instructor &&
  declaration.instructor.id === loggedUser.value.id &&
  declaration.status === "AWAITING_INSTRUCTION"
</script>

<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
.fr-table :deep(.fr-tag) {
  @apply bg-gray-200!;
}
/* On surcharge les couleurs dans `index.css` car pour les instructeur.ices les points d'attentions sont différents */
.fr-table :deep(.fr-tag.AWAITING_INSTRUCTION) {
  @apply bg-amber-100!;
}
.fr-table :deep(.fr-tag.ONGOING_INSTRUCTION) {
  @apply bg-blue-france-925!;
}
</style>
