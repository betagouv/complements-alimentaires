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
      rowData: [d.name, getStatusTagForCell(d.status)],
    }))

  return sorted.map((d) => ({
    rowData: [
      {
        component: "router-link",
        text: d.name,
        to: { name: "DeclarationPage", params: { id: d.id } },
      },
      d.brand || "—",
      getStatusTagForCell(d.status),
      timeAgo(d.modificationDate),
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
.fr-table :deep(table) {
  @apply !table;
}
</style>
