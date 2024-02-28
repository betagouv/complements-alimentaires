<template>
  <DsfrTable noCaption title="Substances" :headers="headers" :rows="rows" />
</template>

<script setup>
import { computed } from "vue"
const props = defineProps({
  substances: Array,
})
const headers = ["Nom", "Numéro CAS", "Numéro EINEC"]
const rows = computed(() => props.substances.map((x) => [x.name.toLowerCase(), x.casNumber, x.einecNumber]))
</script>

<style scoped>
div:deep(table) {
  @apply !table;
}
div:deep(td) {
  @apply capitalize;
}
</style>
