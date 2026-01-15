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
import { articleOptionsWith15Subtypes } from "@/utils/mappings"
import CompanyTableCell from "@/components/CompanyTableCell"
import SpanCell from "@/components/SpanCell"

const props = defineProps({ data: { type: Object, default: () => {} } })

const headers = [
  "ID",
  "Nom du produit",
  "Entreprise",
  "État",
  "Date limite de réponse",
  "Instruit par",
  "Visé par",
  "Article",
]
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowData: [
      x.id,
      {
        component: "router-link",
        text: x.name,
        to: { name: "VisaPage", params: { declarationId: x.id } },
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
        : { component: SpanCell, text: "Non-assigné", class: "italic" },
      x.visor
        ? `${x.visor.firstName} ${x.visor.lastName}`
        : { component: SpanCell, text: "Non-assigné", class: "italic" },
      x.article ? articleOptionsWith15Subtypes.find((y) => y.value === x.article)?.shortText : "",
    ],
  }))
)
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
.fr-table :deep(.fr-tag.AWAITING_VISA) {
  @apply bg-amber-100!;
}
.fr-table :deep(.fr-tag.ONGOING_VISA) {
  @apply bg-blue-france-925!;
}
</style>
