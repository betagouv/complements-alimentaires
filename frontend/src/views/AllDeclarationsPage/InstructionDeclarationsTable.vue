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

const props = defineProps({ data: { type: Object, default: () => {} } })

const headers = ["Nom du produit", "Entreprise", "Auteur", "État de la déclaration", "Date de modification"]
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowData: [
      {
        component: "router-link",
        text: x.name,
        to: { name: "DeclarationPage", params: { id: x.id } },
      },
      x.company.socialName,
      `${x.author.firstName} ${x.author.lastName}`,
      getStatusTagForCell(x.status),
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
