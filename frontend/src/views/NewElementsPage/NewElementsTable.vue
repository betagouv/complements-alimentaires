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
  "Déclaration",
]
const rows = computed(() =>
  props.data.results?.map((x) => ({
    rowData: [
      x.name,
      getTypeInFrench(x.type),
      getAuthorizationModeInFrench(x.authorizationMode),
      x.declaration.creationDate && isoToPrettyDate(x.declaration.creationDate),
      getStatusTagForCell(x.declaration.status),
      // TODO: replace with link to request view
      {
        component: "router-link",
        text: x.declaration.name,
        to: { name: "InstructionPage", params: { declarationId: x.declaration.id } },
      },
    ],
  }))
)
</script>
