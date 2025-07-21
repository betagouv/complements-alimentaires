<template>
  <div>
    <DsfrTable ref="table" title="Les entreprises" :rows="rows" :no-caption="true" :pagination="false">
      <template #header>
        <TableHeaders :headers="headers" />
      </template>
    </DsfrTable>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { getCompanyActivitiesString } from "@/utils/mappings"
import TableHeaders from "@/components/TableHeaders"

const emit = defineEmits(["sort"])

const props = defineProps({ data: { type: Object, default: () => {} } })
const headers = computed(() => [
  {
    text: "Entreprise",
    sortParam: "socialName",
    sortCallback: (value) => emit("sort", value),
    ariaLabel: "Trier par nom de l'entreprise",
  },
  {
    text: "Code postal",
    sortParam: "postalCode",
    sortCallback: (value) => emit("sort", value),
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

// Construction des files de la table
const rows = computed(() =>
  props.data?.results?.map((x) => ({
    rowData: [
      {
        component: "router-link",
        text: x.socialName,
        class: "font-bold",
        to: { name: "CompanyDetails", params: { companyId: x.id } },
      },
      x.postalCode,
      getCompanyActivitiesString(x.activities || []),
      // "",
      // "",
      // "",
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
