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
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"

const { loggedUser } = storeToRefs(useRootStore())

const props = defineProps({ data: { type: Object, default: () => {} } })

const headers = ["", "Nom du produit", "Entreprise", "État de la déclaration", "Date de modification", "Instruit par"]
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowAttrs: { class: needsAttention(x) ? "font-bold" : "" },
    rowData: [
      needsAttention(x) ? { component: "div", class: "h-3 w-3 rounded-full bg-orange-400" } : "",
      {
        component: "router-link",
        text: x.name,
        to: { name: "InstructionPage", params: { declarationId: x.id } },
      },
      x.company.socialName,
      getStatusTagForCell(x.status),
      timeAgo(x.modificationDate),
      x.instructor
        ? `${x.instructor.firstName} ${x.instructor.lastName}`
        : { component: "span", text: "Non-assigné", class: "italic" },
    ],
  }))
)

const needsAttention = (declaration) =>
  !!declaration.instructor &&
  declaration.instructor.id === loggedUser.value.id &&
  declaration.status === "AWAITING_INSTRUCTION"
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
