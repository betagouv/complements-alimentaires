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
import { getAuthorizationModeInFrench } from "@/utils/mappings"
import TypeName from "./TypeName"

const props = defineProps({ data: { type: Object, default: () => {} } })

const headers = [
  "Entreprise",
  "Nom de l'ingrédient",
  "Type d'ingrédient",
  "Authorisation marché FR ou EU",
  "Date limite de réponse",
  "Statut de la déclaration",
  "Statut de la demande",
  "",
]
const rows = computed(() =>
  props.data.results?.map((x) => ({
    rowData: [
      x.declaration.company?.socialName,
      x.name,
      {
        component: TypeName,
        element: x,
      },
      getAuthorizationModeInFrench(x.authorizationMode),
      x.declaration.responseLimitDate && isoToPrettyDate(x.declaration.responseLimitDate),
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
  const status = {
    REQUESTED: {
      label: "Nouvelle",
      type: "info",
    },
    INFORMATION: {
      label: "Information",
      type: "warning",
    },
    REJECTED: {
      label: "Refusé",
      type: "error",
    },
    REPLACED: {
      label: "Remplacé",
      type: "success",
    },
  }[request.requestStatus]

  return (
    status && {
      ...status,
      component: "DsfrBadge",
    }
  )
}
</script>

<style scoped>
.fr-table :deep(td) {
  width: calc(100% / 6);
}
</style>
