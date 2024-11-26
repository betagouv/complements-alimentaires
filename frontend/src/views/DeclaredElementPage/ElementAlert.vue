<template>
  <DsfrAlert v-if="alert" v-bind="alert" class="mb-4" />
</template>

<script setup>
import { computed } from "vue"
const props = defineProps({ element: Object })

const alerts = computed(() => ({
  REQUESTED: {
    title: "Nouvel ingrédient",
    description: "Ingrédient non intégré dans la base de données et en attente de validation.",
    type: "info",
  },
  INFORMATION: {
    title: "Attente d'information",
    description: props.element?.requestPrivateNotes,
    type: "warning",
  },
  REJECTED: {
    title: "Ingrédient refusé",
    description: props.element?.requestPrivateNotes,
    type: "error",
  },
}))
const alert = computed(() => alerts.value[props.element?.requestStatus])
</script>
