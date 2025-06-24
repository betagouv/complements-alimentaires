<template>
  <DsfrAlert v-if="alert" v-bind="alert" class="mb-4">
    <span v-if="alert.description">{{ alert.description }}</span>
    <span v-else-if="element.isPartRequest && element.requestStatus === 'REPLACED'">
      Partie de plante autorisée pour
      <router-link :to="elementLink">{{ element.element.name }}</router-link>
      dans la composition de la déclaration.
    </span>
    <span v-else-if="element.requestStatus === 'REPLACED'">
      Ingrédient initial remplacé par
      <router-link :to="elementLink">{{ element.element.name }}</router-link>
      dans la composition de la déclaration.
    </span>
  </DsfrAlert>
</template>

<script setup>
import { computed } from "vue"
import { getElementUrlComponent } from "@/utils/elements"

const props = defineProps({ element: Object })

const alerts = computed(() => {
  if (props.element?.isPartRequest) {
    return {
      REQUESTED: {
        title: "Nouvelle partie de plante",
        description: "Partie de plante non associée ou non autorisée et en attente de validation.",
        type: "info",
      },
      INFORMATION: {
        title: "En attente d'information",
        description: props.element?.requestPrivateNotes,
        type: "warning",
      },
      REJECTED: {
        title: "Partie de plante refusée",
        description: props.element?.requestPrivateNotes,
        type: "error",
      },
      REPLACED: {
        title: "Partie de plante acceptée",
        type: "success",
      },
    }
  }
  return {
    REQUESTED: {
      title: "Nouvel ingrédient",
      description: "Ingrédient non intégré dans la base de données et en attente de validation.",
      type: "info",
    },
    INFORMATION: {
      title: "En attente d'information",
      description: props.element?.requestPrivateNotes,
      type: "warning",
    },
    REJECTED: {
      title: "Ingrédient refusé",
      description: props.element?.requestPrivateNotes,
      type: "error",
    },
    REPLACED: {
      title: "Ingrédient remplacé",
      type: "success",
    },
  }
})
const alert = computed(() => alerts.value[props.element?.requestStatus])

const elementLink = computed(() => {
  if (!props.element?.element) return
  return {
    name: "ElementPage",
    params: { urlComponent: getElementUrlComponent(props.element.element, props.element.type) },
  }
})
</script>
