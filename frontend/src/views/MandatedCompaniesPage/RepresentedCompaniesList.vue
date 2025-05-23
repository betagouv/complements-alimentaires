<template>
  <div>
    <DsfrTable
      ref="table"
      class="w-full"
      title="Entreprises representées"
      :headers="headers"
      :rows="rows"
      :no-caption="true"
      :pagination="false"
    />
  </div>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({ companies: Array })
const orderedCompanies = computed(() => [...props.companies].sort((a, b) => a.socialName.localeCompare(b.socialName)))

const getRow = (c) => ({ rowData: [c.socialName, c.siret || "—", c.vat || "—"] })

const headers = ["Entreprise", "SIRET", "Numéro de TVA"]
const rows = computed(() => orderedCompanies.value.map(getRow))
</script>

<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
</style>
