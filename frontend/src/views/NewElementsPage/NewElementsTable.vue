<template>
  <DsfrTable
    ref="table"
    class="w-full"
    title="Liste des demandes en attente d’ajout d’ingrédients"
    :headers="headers"
    :rows="rows"
    :no-caption="true"
    :pagination="false"
  />
</template>

<script setup>
import { computed } from "vue"
import { isoToPrettyDate } from "@/utils/date"
import { getStatusTagForCell } from "@/utils/components"
import { getTypeInFrench, getAuthorizationModeInFrench } from "@/utils/mappings"

const props = defineProps({ data: { type: Object, default: () => {} } })

const headers = [
  "Nom de l'ingrédient",
  "Type d'ingrédient",
  "Authorisation marché FR ou EU",
  "Date de demande d'ajout",
  "Statut de la déclaration",
  "Statut de la demande",
  "",
]
const rows = computed(() =>
  props.data.results?.map((x) => ({
    rowData: [
      x.name,
      getTypeInFrench(x.type),
      getAuthorizationModeInFrench(x.authorizationMode),
      x.declaration.creationDate && isoToPrettyDate(x.declaration.creationDate),
      getStatusTagForCell(x.declaration.status),
      getRequestStatusTagForCell(x),
      {
        component: "router-link",
        text: "Contrôler l'ingrédient",
        to: { name: "DeclaredElementPage", params: { type: x.type, id: x.id } },
      },
    ],
  }))
)

const getRequestStatusTagForCell = (request) => {
  // TODO: ideally reuse the DSFR icons used in the alerts, but unsure if those classes are working
  const status = {
    REQUESTED: {
      label: "Nouvelle",
      icon: "ri-todo-fill",
      class: "info",
    },
    INFORMATION: {
      label: "Information",
      icon: "ri-time-line",
      class: "warning",
    },
    REJECTED: {
      label: "Refusé",
      icon: "ri-error-warning-line",
      class: "error",
    },
  }[request.requestStatus]

  return status
    ? {
        ...status,
        component: "DsfrTag",
      }
    : {}
}
</script>

<style scoped>
.fr-table :deep(td) {
  width: calc(100% / 6);
}

:deep(.info) {
  color: var(--info-425-625);
  background-color: var(--info-950-100);
}
:deep(.error) {
  color: var(--error-425-625);
  background-color: var(--error-950-100);
}
:deep(.warning) {
  color: var(--warning-425-625);
  background-color: var(--warning-950-100);
}
</style>
