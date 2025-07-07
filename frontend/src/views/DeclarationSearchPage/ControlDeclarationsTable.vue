<template>
  <div>
    <DsfrTable ref="table" title="Toutes les déclarations" :rows="rows" :no-caption="true" :pagination="false">
      <template #header>
        <TableHeaders :headers="headers" />
      </template>
    </DsfrTable>
    <DsfrModal
      title="Filtrer par statut"
      :opened="statusModalOpened"
      @close="applyStatusModal"
      :actions="statusModalActions"
    >
      <DsfrCheckboxSet v-model="filteredStatuses" :options="options" />
    </DsfrModal>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import { isoToPrettyDate } from "@/utils/date"
import { getStatusTagForCell } from "./utils"
import { useRoute } from "vue-router"
import TableHeaders from "@/components/TableHeaders"

const route = useRoute()
const emit = defineEmits(["sort", "filter"])

const props = defineProps({ data: { type: Object, default: () => {} } })
const headers = computed(() => [
  { text: "ID décla." },
  {
    text: "Produit",
    onClick: () => sortBy("name"),
    active: currentSort.value === "name",
    icon: getSortIcon("name"),
    ariaLabel: "Trier par nom de produit",
  },
  {
    text: "Entreprise",
    onClick: () => sortBy("companyName"),
    active: currentSort.value === "companyName",
    icon: getSortIcon("companyName"),
    ariaLabel: "Trier par nom de l'entreprise",
  },

  { text: "Marque" },
  {
    text: "Statut du produit",
    onClick: () => (statusModalOpened.value = true),
    active: filteredStatuses.value.length,
    icon: "ri-filter-line",
    ariaLabel: "Filtrer par statut du produit",
  },
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
const getSortIcon = (sortParam) =>
  currentSort.value === sortParam
    ? sortDirection.value === "+"
      ? "ri-sort-desc"
      : "ri-sort-asc"
    : "ri-arrow-up-down-line"

// Gestion du filtrage
const filterBy = (filterParam, filterValue) => emit("filter", filterParam, filterValue)

// Construction des files de la table
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowData: [
      x.id || x.siccrfId || x.teleicareDeclarationNumber,
      { component: "span", text: x.name, class: "font-bold" },
      x.companyName,
      x.brand,
      getStatusTagForCell(x.simplifiedStatus),
      x.simplifiedStatusDate ? isoToPrettyDate(x.simplifiedStatusDate) : "",
    ],
  }))
)

// filtrage de statut
const simplifiedStatuses = [
  "Commercialisation possible",
  "En cours d'instruction",
  "Commercialisation refusée",
  "Retiré du marché",
  "Instruction interrompue",
]
const options = simplifiedStatuses.map((x) => ({ label: x, value: x, tagLabel: x }))
const statusModalOpened = ref(false)
const filteredStatuses = ref(route.query.simplifiedStatus.split(",").filter((x) => !!x))
const applyStatusModal = () => {
  filterBy("simplifiedStatus", filteredStatuses.value.join(","))
  statusModalOpened.value = false
}

const statusModalActions = [
  {
    label: "Appliquer",
    onClick: applyStatusModal,
  },
  {
    label: "Annuler",
    secondary: true,
    onClick: () => (statusModalOpened.value = false),
  },
]
</script>

<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
</style>
