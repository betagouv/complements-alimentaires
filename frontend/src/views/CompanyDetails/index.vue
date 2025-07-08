<template>
  <div class="fr-container mb-10">
    <DsfrBreadcrumb
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: previousRoute, text: 'Recherche entreprises' },
        { text: company?.socialName || 'Résultat' },
      ]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="company">
      <h1>{{ company.socialName }}</h1>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { onMounted, computed } from "vue"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"

const router = useRouter()
const previousRoute = computed(() => {
  const previousRoute = router.getPreviousRoute().value
  return previousRoute?.name === "CompanySearchPage" ? previousRoute : { name: "CompanySearchPage" }
})

const props = defineProps({ companyId: String })

const {
  response: companyResponse,
  data: company,
  execute: executeCompanyFetch,
  isFetching,
} = useFetch(() => `/api/v1/companies/${props.companyId}`, { immediate: false })
  .get()
  .json()

onMounted(async () => {
  await executeCompanyFetch()
  handleError(companyResponse)
})
</script>
