<template>
  <DsfrTable
    ref="table"
    class="w-full"
    title="Toutes les déclarations"
    :headers="headers"
    :rows="rows"
    :no-caption="true"
    :pagination="false"
  />
</template>

<script setup>
import { computed } from "vue"
import { timeAgo } from "@/utils/date"
import { getStatusTagForCell } from "@/utils/components"

const props = defineProps({ data: { type: Object, default: () => {} } })

const headers = ["Nom du produit", "Entreprise", "État", "Date de modification", "Instruit par", "Visé par"]
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowData: [
      {
        component: "router-link",
        text: x.name,
        to: { name: "VisaPage", params: { declarationId: x.id } },
      },
      x.company.socialName,
      getStatusTagForCell(x.status),
      timeAgo(x.modificationDate),
      x.instructor
        ? `${x.instructor.firstName} ${x.instructor.lastName}`
        : { component: "span", text: "Non-assigné", class: "italic" },
      x.visor
        ? `${x.visor.firstName} ${x.visor.lastName}`
        : { component: "span", text: "Non-assigné", class: "italic" },
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
.fr-table :deep(.fr-tag.AWAITING_VISA) {
  @apply !bg-amber-100;
}
.fr-table :deep(.fr-tag.ONGOING_VISA) {
  @apply !bg-blue-france-925;
}
</style>
