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

const props = defineProps({ data: { type: Object, default: () => {} } })
const headers = ["ID décla.", "Produit", "Entreprise", "Marque", "Statut du produit", "Date d'application du statut"]

const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowAttrs: { class: "" },
    rowData: [
      x.id || x.siccrfid || x.teleicareDeclarationNumber,
      { component: "p", text: x.name, class: "font-bold" },
      x.companyName,
      x.brand,
      x.simplifiedStatus,
      isoToPrettyDate(x.simplifiedStatusDate),
    ],
  }))
)
</script>

<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
</style>
