<template>
  <div>
    <h2 class="fr-h6 !mb-1">Quantité maximales autorisées par population</h2>
    <DsfrTable :headers="maxQuantityHeaders" :rows="maxQuantityRows" />
  </div>
</template>

<script setup>
defineProps({
  maxQuantityRows: Object,
})
const maxQuantityHeaders = ["Population", "Quantité maximale"]
</script>
