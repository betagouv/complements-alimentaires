<template>
  <div class="grid grid-cols-2">
    <div class="col-span-2 md:col-span-1 bg-blue-france-975 border px-10 mb-5">
      <div class="fr-h5 !mt-5">Quantité maximales autorisées par population</div>
      <DsfrTable :headers="maxQuantityHeaders" :rows="maxQuantityRows" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  maxQuantityRows: Object,
})
const maxQuantityHeaders = ["Population", "Quantité maximale"]
</script>
<div class="hidden md:flex md:col-span-4 lg:col-span-6 justify-center content-center">
      <DsfrTable
        title="Quantité maximales autorisées par population"
        :headers="maxQuantityHeaders"
        :rows="maxQuantityRows"
      />
    </div>
#f5f5fe
