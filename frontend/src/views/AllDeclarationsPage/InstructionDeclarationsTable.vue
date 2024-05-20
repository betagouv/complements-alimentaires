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
import { computed } from "vue"
import { timeAgo } from "@/utils/date"
import { getStatusTagForCell } from "@/utils/components"

const props = defineProps({ data: { type: Object, default: () => {} } })
const emit = defineEmits("open")

const headers = ["Nom du produit", "Entreprise", "Auteur", "État de la déclaration", "Date de modification"]
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowAttrs: { class: "cursor-pointer", onClick: () => emit("open", x.id) },
    rowData: [
      x.name,
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
