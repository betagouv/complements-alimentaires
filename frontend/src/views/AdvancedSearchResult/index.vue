<template>
  <div class="fr-container mb-10">
    <DsfrBreadcrumb
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: { name: 'AdvancedSearchPage' }, text: 'Recherche avancée' },
        { text: 'Déclaration' },
      ]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <DeclarationSummary :readonly="true" v-if="declaration" v-model="declaration" />
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { onMounted, ref } from "vue"
import { useRootStore } from "@/stores/root"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import DeclarationSummary from "@/components/DeclarationSummary"

const store = useRootStore()
store.fetchDeclarationFieldsData()

const props = defineProps({
  declarationId: String,
})

// Requêtes
const {
  response: declarationResponse,
  data: declaration,
  isFetching,
  execute: executeDeclarationFetch,
} = useFetch(`/api/v1/declarations/${props.declarationId}`, { immediate: false }).get().json()

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)
})
</script>
