<template>
  <DsfrTable ref="table" title="Toutes les déclarations" :rows="rows" :no-caption="true" :pagination="false">
    <template #header>
      <!-- Il faut générer programmatiquement les entêtes à cause du bug : https://github.com/dnum-mi/vue-dsfr/issues/1091 -->
      <tr>
        <DsfrTableHeader
          :header="header.text"
          :header-attrs="header.headerAttrs"
          :icon="header.icon"
          v-for="header in headers"
          :key="header.text"
        />
      </tr>
    </template>
  </DsfrTable>
</template>

<script setup>
import { computed, ref } from "vue"
import { isoToPrettyDate } from "@/utils/date"
import { getStatusTagForCell } from "./utils"

const props = defineProps({ data: { type: Object, default: () => {} } })
const headers = computed(() => [
  { text: "ID décla." },
  { text: "Produit", headerAttrs: getSortHeaderAttrs("name"), icon: getSortIcon("name") },
  { text: "Entreprise", headerAttrs: getSortHeaderAttrs("company"), icon: getSortIcon("company") },
  { text: "Marque", headerAttrs: getFilterHeaderAttrs("brand"), icon: "ri-filter-line" },
  { text: "Statut du produit", headerAttrs: getFilterHeaderAttrs("status"), icon: "ri-filter-line" },
  { text: "Date d'application du statut" },
])

// Gestion du triage
const currentSort = ref()
const sortDirection = ref()
const sortBy = (sortParam) => console.log(`Sort by ${sortParam}`)
const getSortHeaderAttrs = (sortParam) => ({ class: "cursor-pointer", onClick: () => sortBy(sortParam) })
const getSortIcon = (sortParam) =>
  currentSort.value === sortParam
    ? sortDirection.value === "+"
      ? "ri-sort-asc"
      : "ri-sort-desc"
    : "ri-arrow-up-down-line"

// Gestion du filtrage
const getFilterHeaderAttrs = (filterParam) => ({ class: "cursor-pointer", onClick: () => filterBy(filterParam) })
const filterBy = (filterParam, filterValue) => console.log(`Filter by ${filterParam} : ${filterValue}`)

const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowAttrs: { class: "" },
    rowData: [
      x.id || x.siccrfid || x.teleicareDeclarationNumber,
      { component: "p", text: x.name, class: "font-bold" },
      x.companyName,
      x.brand,
      getStatusTagForCell(x.simplifiedStatus),
      x.simplifiedStatusDate ? isoToPrettyDate(x.simplifiedStatusDate) : "",
    ],
  }))
)
</script>

<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
.fr-table :deep(th .vicon) {
  @apply ml-2!;
}
</style>
