<template>
  <ul class="list-none">
    <SummaryElementItem
      class="mb-2 last:mb-0"
      v-for="(element, index) in elements"
      :key="`summary-${objectType}-${index}`"
      v-model="elements[index]"
      :objectType="objectType"
      :showElementAuthorization="showElementAuthorization"
    />
  </ul>
</template>

<script setup>
import SummaryElementItem from "./SummaryElementItem"

defineProps({ objectType: { type: String }, elements: { type: Array }, showElementAuthorization: { type: Boolean } })
</script>
