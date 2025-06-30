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
import { useRoute } from "vue-router"

const route = useRoute()
const emit = defineEmits(["sort", "filter"])

const props = defineProps({ data: { type: Object, default: () => {} } })
const headers = computed(() => [
  { text: "ID décla." },
  { text: "Produit", headerAttrs: getSortHeaderAttrs("name"), icon: getSortIcon("name") },
  { text: "Entreprise", headerAttrs: getSortHeaderAttrs("companyName"), icon: getSortIcon("companyName") },

  { text: "Marque" },
  { text: "Statut du produit" },

  // Remplacer les deux lignes précedentes par celles-ci lors que le filtrage sera mis en place
  // { text: "Marque", headerAttrs: getFilterHeaderAttrs("brand"), icon: "ri-filter-line" },
  // { text: "Statut du produit", headerAttrs: getFilterHeaderAttrs("status"), icon: "ri-filter-line" },

  { text: "Date d'application du statut" },
])

// Gestion du triage
const currentSort = ref(route.query.triage ? route.query.triage.substring(1) : undefined)
const sortDirection = ref(route.query.triage ? route.query.triage.substring(0, 1) : undefined)
const sortBy = (sortParam) => {
  if (currentSort.value === sortParam) {
    if (!sortDirection.value) sortDirection.value = "+"
    else if (sortDirection.value === "+") sortDirection.value = "-"
    else sortDirection.value = currentSort.value = "" // Si on a cliqué trois fois on désactive le triage
  } else {
    sortDirection.value = "+"
    currentSort.value = sortParam
  }
  emit("sort", `${sortDirection.value}${currentSort.value}`)
}
const getSortHeaderAttrs = (sortParam) => ({ class: "cursor-pointer", onClick: () => sortBy(sortParam) })
const getSortIcon = (sortParam) =>
  currentSort.value === sortParam
    ? sortDirection.value === "+"
      ? "ri-sort-desc"
      : "ri-sort-asc"
    : "ri-arrow-up-down-line"

// Gestion du filtrage
// Activer les lignes suivantes lors que le filtrage sera mis en place
// const getFilterHeaderAttrs = (filterParam) => ({ class: "cursor-pointer", onClick: () => filterBy(filterParam) })
// const filterBy = (filterParam, filterValue) => console.log(`Filter by ${filterParam} : ${filterValue} not implemented`)

// Construction des files de la table
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
