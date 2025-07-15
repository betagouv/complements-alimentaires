<template>
  <div class="fr-container mb-10">
    <!-- TODO : Get breadcrumbs list dynamically from previous route -->
    <DsfrBreadcrumb
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: previousRoute, text: 'Recherche entreprises' },
        { text: declaration?.name || 'Complément alimentaire' },
      ]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="declaration">
      <h1>{{ declaration.name }}</h1>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
import { computed, onMounted } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"

const router = useRouter()
const previousRoute = computed(() => {
  const previousRoute = router.getPreviousRoute().value
  return previousRoute?.name === "CompanySearchPage" ? previousRoute : { name: "CompanySearchPage" }
})

const props = defineProps({ declarationId: String })

const {
  response: declarationResponse,
  data: declaration,
  execute: executeDeclarationFetch,
  isFetching,
} = useFetch(() => `/api/v1/control/declarations/${props.declarationId}`, { immediate: false })
  .get()
  .json()

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)
})
</script>
