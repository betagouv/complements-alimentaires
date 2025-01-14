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
import { timeAgo } from "@/utils/date"
import { getStatusTagForCell } from "@/utils/components"
import CompanyTableCell from "@/components/CompanyTableCell"

const props = defineProps({ data: { type: Object, default: () => {} } })

const headers = ["ID", "Nom du produit", "Entreprise", "Auteur", "État", "Date de création", "Date de modification"]
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowData: [
      x.declaredInTeleicare
        ? {
            component: "DsfrBadge",
            label: "issue de Teleicare",
            type: "info",
            small: true,
            noIcon: true,
          }
        : x.id,
      {
        component: "router-link",
        text: x.name,
        to: { name: "DeclarationPage", params: { id: x.id } }, // TODO Change to a more enteprisey view
      },
      {
        component: CompanyTableCell,
        company: x.company?.socialName,
        mandatedCompany: x.mandatedCompany?.socialName,
      },
      x.author ? `${x.author.firstName} ${x.author.lastName}` : "",
      getStatusTagForCell(x.status, true),
      timeAgo(x.creationDate),
      timeAgo(x.modificationDate),
    ],
  }))
)
</script>

<style scoped>
.fr-table :deep(table) {
  @apply !table;
}
</style>
