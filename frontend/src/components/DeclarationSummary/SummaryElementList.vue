<template>
  <div v-if="elements.length">
    <!-- Affichage avec les accordéons : les ingrédients sont cachés à l'intérieur -->
    <DsfrAccordion v-if="useAccordions">
      <template v-slot:title>
        <SummaryElementListTitle :objectType="objectType" :elementCount="`${elements.length}`" />
      </template>
      <SummaryElementListItems :objectType="objectType" :elements="elements" />
    </DsfrAccordion>

    <!-- Affichage sans les accordéons, tous les ingrédients sont affichés -->
    <div v-else>
      <SummaryElementListTitle class="mt-6 mb-3" :objectType="objectType" />
      <SummaryElementListItems :objectType="objectType" :elements="elements" />
    </div>
  </div>
</template>

<script setup>
import SummaryElementListTitle from "./SummaryElementListTitle"
import SummaryElementListItems from "./SummaryElementListItems"

defineProps({ objectType: { type: String }, elements: { type: Array }, useAccordions: { type: Boolean } })
</script>
