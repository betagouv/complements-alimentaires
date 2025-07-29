<template>
  <div>
    <DsfrBadge :label="warningText" type="warning" small v-if="warningText" />
    <div>
      <router-link
        class="font-bold"
        :to="{ name: 'DeclarationIndividualPage', params: { declarationId: declaration.id } }"
      >
        {{ declaration.name }}
      </router-link>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ declaration: Object })

import { computed } from "vue"

const warningText = computed(() => {
  if (props.declaration.article === "ART_15_WARNING") return "À surveiller"
  if (props.declaration.article === "ART_15_HIGH_RISK_POPULATION") return "Population à risque"
  if (props.declaration.article === "ART_16") return "Nouvel ingrédient ajouté"
  return null
})
</script>
