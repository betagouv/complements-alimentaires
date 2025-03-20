<template>
  <div class="fr-container mb-10">
    <DsfrBreadcrumb
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: previousRoute, text: 'Recherche avancée' },
        { text: declaration?.name || 'Résultat' },
      ]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else>
      <h1 class="fr-text--sm font-normal !mb-0">Résultat de la recherche</h1>
      <h2>{{ declaration?.name }}</h2>

      <DeclarationSummary :readonly="true" v-if="declaration" v-model="declaration" />
    </div>
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { onMounted, computed } from "vue"
import { useRouter } from "vue-router"
import { useRootStore } from "@/stores/root"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import DeclarationSummary from "@/components/DeclarationSummary"

const store = useRootStore()
store.fetchDeclarationFieldsData()

const router = useRouter()
const previousRoute = computed(() => {
  const previousRoute = router.getPreviousRoute().value
  return previousRoute?.name === "AdvancedSearchPage" ? previousRoute : { name: "AdvancedSearchPage" }
})

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
