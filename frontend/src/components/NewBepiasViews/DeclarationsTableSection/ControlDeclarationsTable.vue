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
import { getStatusTagForCell } from "@/components/NewBepiasViews/DeclarationsTableSection/utils"
import { useRoute } from "vue-router"
import TableHeaders from "@/components/TableHeaders"
import NameCell from "./NameCell"

const route = useRoute()
const emit = defineEmits(["sort", "filter"])

const props = defineProps({ data: { type: Object, default: () => {} } })
const headers = computed(() => [
  { text: "ID décla." },
  {
    text: "Produit",
    sortParam: "name",
    sortCallback: (value) => emit("sort", value),
    ariaLabel: "Trier par nom de produit",
  },
  {
    text: "Entreprise",
    sortParam: "companyName",
    sortCallback: (value) => emit("sort", value),
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

// Gestion du filtrage
const filterBy = (filterParam, filterValue) => emit("filter", filterParam, filterValue)

// Construction des files de la table
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowData: [
      x.id || x.siccrfId || x.teleicareDeclarationNumber,
      {
        component: NameCell,
        declaration: x,
      },
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
@reference "../../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
</style>
