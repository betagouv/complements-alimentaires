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
import { statusProps } from "@/utils/mappings"
import { useResizeObserver, useDebounceFn } from "@vueuse/core"

const props = defineProps({ data: { type: Array, default: () => [] } })
const emit = defineEmits("open")

// Les données pour la table
const headers = computed(() => {
  if (useShortTable.value) return ["Nom", "État"]
  return ["Nom du produit", "Marque", "État de la déclaration", "Date de modification"]
})
const rows = computed(() => {
  // Les dates ISO sont sortables par text
  if (!props.data) return []
  const sorted = [...props.data].sort((a, b) => b.modificationDate.localeCompare(a.modificationDate))

  if (useShortTable.value)
    return sorted.map((d) => ({
      rowAttrs: { class: "cursor-pointer", onClick: () => emit("open", d.id) },
      rowData: [d.name, getTagForCell(d.status)],
    }))

  return sorted.map((d) => ({
    rowAttrs: { class: "cursor-pointer", onClick: () => emit("open", d.id) },
    rowData: [d.name, d.brand || "—", getTagForCell(d.status), timeAgo(d.modificationDate)],
  }))
})

const getTagForCell = (status) => ({
  component: "DsfrTag",
  label: statusProps[status].label,
  class: status,
  icon: statusProps[status].icon,
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
.fr-table :deep(table) {
  @apply !table;
}
.fr-table :deep(.fr-tag .ov-icon) {
  @apply !mr-2;
}
/* Je dois les spécifier ici car Tailwind ne fait pas des classes dynamiques pour le bg */
/* https://stackoverflow.com/questions/72481680/tailwinds-background-color-is-not-being-applied-when-added-dynamically */
.fr-table :deep(.fr-tag.DRAFT) {
  @apply !bg-blue-france-925;
}
.fr-table :deep(.fr-tag.AWAITING_INSTRUCTION) {
  @apply !bg-gray-200;
}
.fr-table :deep(.fr-tag.AWAITING_PRODUCER) {
  @apply !bg-amber-100;
}
.fr-table :deep(.fr-tag.REJECTED) {
  @apply !bg-red-marianne-925;
}
.fr-table :deep(.fr-tag.APPROVED) {
  @apply !bg-success-950;
}
</style>
