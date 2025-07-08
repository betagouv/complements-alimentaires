<template>
  <div>
    <DsfrTable ref="table" title="Toutes les déclarations" :rows="rows" :no-caption="true" :pagination="false">
      <template #header>
        <TableHeaders :headers="headers" />
      </template>
    </DsfrTable>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import { useRoute } from "vue-router"
import { allActivities } from "@/utils/mappings"
import TableHeaders from "@/components/TableHeaders"

const route = useRoute()
const emit = defineEmits(["sort"])

const props = defineProps({ data: { type: Object, default: () => {} } })
const headers = computed(() => [
  {
    text: "Entreprise",
    onClick: () => sortBy("socialName"),
    active: currentSort.value === "socialName",
    icon: getSortIcon("socialName"),
    ariaLabel: "Trier par nom de l'entreprise",
  },
  {
    text: "Code postal",
    onClick: () => sortBy("postalCode"),
    active: currentSort.value === "postalCode",
    icon: getSortIcon("postalCode"),
    ariaLabel: "Trier par code postale",
  },
  {
    text: "Rôles",
  },
  // {
  //   text: "Nb. de produits commercialisables",
  // },
  // {
  //   text: "Nb. de produits avec restrictions",
  // },
  // {
  //   text: "Date de la dernière déclaration",
  // },
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

// Construction des files de la table
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowData: [
      { component: "span", text: x.socialName, class: "font-bold" },
      x.postalCode,
      getActivitiesString(x.activities || []),
      // "",
      // "",
      // "",
    ],
  }))
)

const getActivitiesString = (activities) =>
  activities
    .map((x) => allActivities.find((y) => y.value === x).label)
    .sort((a, b) => a.localeCompare(b))
    .join(", ")
</script>

<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
</style>
