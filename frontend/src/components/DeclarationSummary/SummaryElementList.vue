<template>
  <div v-if="elements.length">
    <!-- Affichage avec les accordéons : les ingrédients sont cachés à l'intérieur -->
    <DsfrAccordionsGroup v-if="useAccordions" v-model="activeAccordion">
      <DsfrAccordion>
        <template v-slot:title>
          <SummaryElementListTitle :objectType="objectType" :elementCount="`${elements.length}`" />
        </template>
        <SummaryElementListItems
          :showElementAuthorization="showElementAuthorization"
          :objectType="objectType"
          :elements="elements"
        />
      </DsfrAccordion>
    </DsfrAccordionsGroup>
    <!-- Affichage sans les accordéons, tous les ingrédients sont affichés -->
    <div v-else>
      <SummaryElementListTitle class="mt-6 mb-3" :objectType="objectType" />
      <SummaryElementListItems
        :showElementAuthorization="showElementAuthorization"
        :objectType="objectType"
        :elements="elements"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import SummaryElementListTitle from "./SummaryElementListTitle"
import SummaryElementListItems from "./SummaryElementListItems"

defineProps({
  objectType: { type: String },
  elements: { type: Array },
  useAccordions: { type: Boolean },
  showElementAuthorization: { type: Boolean },
})

const activeAccordion = ref()
</script>
