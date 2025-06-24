<template>
  <div>
    {{ getTypeInFrench(element.type) }}
    <DsfrBadge v-if="element.newPart" label="Nouvelle partie" />
  </div>
</template>

<script setup>
import { getTypeInFrench } from "@/utils/mappings"

const props = defineProps({
  element: { type: Object },
})
</script>
