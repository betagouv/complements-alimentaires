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
const props = defineProps({ data: { type: Object, default: () => {} } })
const headers = ["Id", "T - ID", "SICCRF - ID"]

const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowAttrs: { class: "" },
    rowData: [x.id, x.teleicareDeclarationNumber, x.siccrfid],
  }))
)
</script>

<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
</style>
