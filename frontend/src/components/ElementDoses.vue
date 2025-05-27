<template>
  <div>
    <h2 class="fr-h6 mb-1!">Quantités maximales autorisées par population</h2>
    <DsfrTable :headers="maxQuantityHeaders" :rows="maxQuantityRows" />
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  maxQuantities: Array,
  unit: String,
})
const maxQuantityHeaders = ["Population", "Quantité maximale"]

const maxQuantityRows = computed(() => {
  return JSON.parse(JSON.stringify(props.maxQuantities))
    .sort((a, b) => b.maxQuantity - a.maxQuantity)
    .map((q) => [q.population?.name, quantityCell(q)])
})

const quantityCell = (row) => {
  return row.maxQuantity === 0
    ? {
        component: "DsfrBadge",
        label: "Non autorisé",
        type: "error",
        small: true,
      }
    : row.maxQuantity?.toLocaleString("fr-FR") + " " + props.unit
}
</script>
