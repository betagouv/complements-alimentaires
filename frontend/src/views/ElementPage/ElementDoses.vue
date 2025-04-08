<template>
  <div>
    <h2 class="fr-h6 !mb-1">Quantité maximales autorisées par population</h2>
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
  return props.maxQuantities.map((maxQuantity) => [maxQuantity.populationName, quantityCell(maxQuantity)])
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
