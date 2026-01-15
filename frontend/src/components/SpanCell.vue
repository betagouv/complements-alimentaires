<template>
  <span>{{ text }}</span>
</template>

<script setup>
// Ce composant existe pour appliquer des styles à un cellule d'un DsfrTable
/*
rowData = [
  {
    component: SpanCell,
    text: "Ma phrase ici",
    class: "capitalize",
    id: "un-id-optionnel",
  },
]
*/
defineProps({ text: String })
</script>
