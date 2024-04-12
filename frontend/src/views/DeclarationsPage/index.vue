<template>
  <div class="fr-container">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[{ to: '/tableau-de-bord', text: 'Tableau de bord' }, { text: 'Mes déclarations' }]"
    />
    <div class="block sm:flex items-center mb-8">
      <h1 class="!mb-0 grow">Mes déclarations</h1>
      <DsfrButton v-if="rows.length" label="Nouvelle déclaration" secondary @click="createNewDeclaration" />
    </div>
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <DsfrTable
      ref="table"
      class="w-full"
      v-else-if="rows.length"
      title="Mes déclarations"
      :headers="headers"
      :rows="rows"
      :no-caption="true"
      :pagination="false"
    />
    <div v-else class="mb-8">
      <p>Vous n'avez pas encore créé des déclarations.</p>
      <DsfrButton icon="ri-capsule-fill" label="Créer ma première déclaration" @click="createNewDeclaration" />
    </div>
  </div>
</template>

<script setup>
import { computed, watch, ref } from "vue"
import ProgressSpinner from "@/components/ProgressSpinner"
import { handleError } from "@/utils/error-handling"
import { timeAgo } from "@/utils/date"
import { statusProps } from "@/utils/mappings"
import { useRouter } from "vue-router"
import { useFetch, useResizeObserver, useDebounceFn } from "@vueuse/core"

// const data = []

const { response, data, isFetching } = useFetch("/api/v1/declarations/").get().json()

// Les données pour la table
const headers = computed(() => {
  if (useShortTable.value) return ["Nom", "État"]
  return ["Nom du produit", "Marque", "État de la déclaration", "Date de modification"]
})
const rows = computed(() => {
  // Les dates ISO sont sortables par text
  if (!data.value) return []
  const sorted = [...data.value].sort((a, b) => a.modificationDate.localeCompare(b.modificationDate))

  if (useShortTable.value) return sorted.map((d) => [d.name, getTagForCell(d.status)])

  return sorted.map((d) => [d.name, d.brand || "—", getTagForCell(d.status), timeAgo(d.modificationDate)])
})

const getTagForCell = (status) => ({
  component: "DsfrTag",
  label: statusProps[status].label,
  class: `!bg-${statusProps[status].background}`,
  icon: statusProps[status].icon,
})

// On prend la width de la table pour montrer/cacher les colonnes
const table = ref(null)
const useShortTable = ref(false)
useResizeObserver(
  table,
  useDebounceFn((entries) => (useShortTable.value = entries[0]?.contentRect.width < 600), 50)
)

watch(response, () => handleError(response))

const router = useRouter()
const createNewDeclaration = () => router.push({ name: "ProducerFormPage" })
</script>

<style scoped>
.fr-table :deep(table) {
  @apply !table;
}
.fr-table :deep(.fr-tag .ov-icon) {
  @apply !mr-2;
}
</style>
