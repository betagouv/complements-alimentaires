<template>
  <DsfrTable
    ref="table"
    class="w-full"
    title="Liste de demandes en attente"
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
  "",
]
const rows = computed(() =>
  props.data?.results?.map((x) => ({
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

<style scoped>
.fr-table :deep(table) {
  @apply !table;
}
.fr-table :deep(.fr-tag) {
  @apply !bg-gray-200;
}
/* On surcharge les couleurs dans `index.css` car pour les instructeur.ices les points d'attentions sont différents */
.fr-table :deep(.fr-tag.AWAITING_INSTRUCTION) {
  @apply !bg-amber-100;
}
.fr-table :deep(.fr-tag.ONGOING_INSTRUCTION) {
  @apply !bg-blue-france-925;
}
</style>
