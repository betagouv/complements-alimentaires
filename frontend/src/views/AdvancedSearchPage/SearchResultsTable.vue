<template>
  <DsfrTable
    ref="table"
    class="w-full"
    title="Résultats de recherche"
    :headers="headers"
    :rows="rows"
    :no-caption="true"
    :pagination="false"
  />
</template>

<script setup>
import { computed } from "vue"
import { timeAgo } from "@/utils/date"
import { getStatusTagForCell } from "@/utils/components"
import CompanyTableCell from "@/components/CompanyTableCell"
import DeclarationName from "@/components/DeclarationName"
import { articleOptionsWith15Subtypes } from "@/utils/mappings"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"

const { units } = storeToRefs(useRootStore())

const props = defineProps({ data: { type: Object, default: () => {} } })

const headers = ["ID", "Nom du produit", "Poids/Unité", "Entreprise", "Article", "Statut", "Date de création"]

const rows = computed(() => {
  // Les dates ISO sont sortables par text
  if (!props.data?.results) return []

  return props.data.results.map((d) => ({
    rowData: [
      d.siccrfId ? (d.teleicareId ? d.teleicareId : "") : d.id,
      {
        component: DeclarationName,
        withHistoryBadge: !!d.siccrfId,
        text: d.name,
        class: "font-medium",
        to: { name: "AdvancedSearchResult", params: { declarationId: d.id } },
      },
      getUnitString(d),
      {
        component: CompanyTableCell,
        company: d.company?.socialName,
        mandatedCompany: d.mandatedCompany?.socialName,
      },
      d.article ? articleOptionsWith15Subtypes.find((x) => x.value === d.article)?.shortText : "",
      getStatusTagForCell(d.status, true),
      timeAgo(d.creationDate),
    ],
  }))
})

const getUnitString = (declaration) => {
  if (!declaration?.unitQuantity) return null
  const unitMeasurement = units.value?.find?.((x) => x.id === declaration.unitMeasurement)?.name || "-"
  return `${declaration.unitQuantity} ${unitMeasurement}`
}
</script>
<style scoped>
.fr-table :deep(table) {
  @apply !table;
}
</style>
