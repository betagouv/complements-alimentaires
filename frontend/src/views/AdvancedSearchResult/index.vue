<template>
  <div class="fr-container mb-10">
    <DsfrBreadcrumb
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: { name: 'AdvancedSearchPage' }, text: 'Recherche avancée' },
        { text: 'Déclaration' },
      ]"
    />
    <DeclarationSummary :readonly="true" v-if="declaration" v-model="declaration" />
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { onMounted, computed, ref } from "vue"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import { handleError } from "@/utils/error-handling"
import DeclarationSummary from "@/components/DeclarationSummary"

const router = useRouter()

const store = useRootStore()
store.fetchDeclarationFieldsData()

const props = defineProps({
  declarationId: String,
})

// Requêtes
const isFetching = ref(true)
const {
  response: declarationResponse,
  data: declaration,
  execute: executeDeclarationFetch,
} = useFetch(`/api/v1/declarations/${props.declarationId}`, { immediate: false }).get().json()

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)
})
</script>
