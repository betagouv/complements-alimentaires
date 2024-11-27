<template>
  <DsfrTable
    ref="table"
    class="w-full"
    title="Entreprises mandatées"
    :headers="headers"
    :rows="rows"
    :no-caption="true"
    :pagination="false"
  />
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({ mandatedCompanies: { type: Array, default: () => [] } })
const emit = defineEmits(["remove"])

const orderedCompanies = computed(() =>
  [...props.mandatedCompanies].sort((a, b) => a.socialName.localeCompare(b.socialName))
)

const headers = ["Entreprise", "SIRET", "Numéro de TVA", ""]
const rows = computed(() =>
  orderedCompanies.value.map((x) => ({
    rowData: [
      x.socialName,
      x.siret || "—",
      x.vat || "—",
      {
        component: "dsfr-button",
        label: "Supprimer",
        secondary: true,
        size: "sm",
        icon: "ri-close-fill",
        onclick: () => removeMandatedCompany(x.id),
      },
    ],
  }))
)
const removeMandatedCompany = (companyId) => {
  emit("remove", companyId)
}
</script>

<style scoped>
.fr-table :deep(table) {
  @apply !table;
}
</style>
