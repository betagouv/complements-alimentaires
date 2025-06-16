<template>
  <DsfrTable
    ref="table"
    class="w-full"
    title="Mes déclarations"
    :headers="headers"
    :rows="rows"
    :no-caption="true"
    :pagination="false"
  />
</template>

<script setup>
import { computed, ref } from "vue"
import { timeAgo } from "@/utils/date"
import { getStatusTagForCell } from "@/utils/components"
import CompanyTableCell from "@/components/CompanyTableCell"
import DeclarationName from "@/components/DeclarationName"
import { useResizeObserver, useDebounceFn } from "@vueuse/core"

const props = defineProps({ data: { type: Object, default: () => {} } })
const emit = defineEmits("open")

// Les données pour la table
const headers = computed(() => {
  if (useShortTable.value) return ["Nom", "État"]
  return ["ID", "Nom du produit", "Entreprise", "Déclarant·e", "État", "Date de création", ""]
})

const rows = computed(() => {
  // Les dates ISO sont sortables par text
  if (!props.data?.results) return []

  if (useShortTable.value)
    return props.data.results.map((d) => ({
      rowAttrs: { class: "cursor-pointer", onClick: () => emit("open", d.id) },
      rowData: [d.name, getStatusTagForCell(d.status, true)],
    }))

  return props.data.results.map((d) => ({
    rowData: [
      d.siccrfId ? (d.teleicareDeclarationNumber ? d.teleicareDeclarationNumber : "") : d.id,
      {
        component: DeclarationName,
        withHistoryBadge: !!d.siccrfId,
        text: d.name,
        class: "font-medium",
        to: { name: "DeclarationPage", params: { id: d.id } },
      },
      {
        component: CompanyTableCell,
        company: d.company?.socialName,
        mandatedCompany: d.mandatedCompany?.socialName,
      },
      d.author ? `${d.author.firstName} ${d.author.lastName}` : "",
      getStatusTagForCell(d.status, true),
      timeAgo(d.creationDate),
      {
        component: "router-link",
        text: "Dupliquer",
        to: { name: "NewDeclaration", query: { duplicate: d.id } },
      },
    ],
  }))
})
// On prend la width de la table pour montrer/cacher les colonnes
const table = ref(null)
const useShortTable = ref(false)
useResizeObserver(
  table,
  useDebounceFn((entries) => (useShortTable.value = entries[0]?.contentRect.width < 600), 50)
)
</script>
<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
</style>
