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
import { isoToPrettyDate } from "@/utils/date"
import { getStatusTagForCell } from "@/utils/components"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { articleOptions } from "@/utils/mappings"

const { loggedUser } = storeToRefs(useRootStore())

const props = defineProps({ data: { type: Object, default: () => {} } })

const headers = ["", "ID", "Nom du produit", "Entreprise", "État", "Date limite de réponse", "Instruit par", "Article"]
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowAttrs: { class: needsAttention(x) ? "font-bold" : "" },
    rowData: [
      needsAttention(x) ? { component: "div", class: `h-3 w-3 rounded-full ${circleColor(x)}` } : "",
      x.id,
      {
        component: "router-link",
        text: x.name,
        to: { name: "InstructionPage", params: { declarationId: x.id } },
      },
      x.company.socialName,
      getStatusTagForCell(x.status),
      x.responseLimitDate && isoToPrettyDate(x.responseLimitDate),
      x.instructor
        ? `${x.instructor.firstName} ${x.instructor.lastName}`
        : { component: "span", text: "Non-assigné", class: "italic" },
      x.article ? articleOptions.find((y) => y.value === x.article)?.shortText : "",
    ],
  }))
)

const needsAttention = (declaration) =>
  !!declaration.instructor &&
  declaration.instructor.id === loggedUser.value.id &&
  declaration.status === "AWAITING_INSTRUCTION"

const circleColor = (declaration) => (declaration.visaRefused ? "bg-red-500" : "bg-orange-400")
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
