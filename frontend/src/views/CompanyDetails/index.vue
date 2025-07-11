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
      <div class="grid grid-cols-2 gap-3">
        <div class="col-span-2 sm:col-span-1">
          <h2>Identité entreprise</h2>
          <InfoTable :items="identityItems" />
        </div>
        <div class="col-span-2 sm:col-span-1">
          <h2>Chiffres clés</h2>
          <InfoTable :items="insightsItems" />
        </div>
      </div>
      <!-- Traiter le cas où l'entreprise n'a pas de déclarations  -->
      <h2 class="mt-8">Produits déclarés auprès de la DGAL par cette entreprise</h2>
      <DeclarationsTableSection :companyId="companyId" />
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { onMounted, computed } from "vue"
import { handleError } from "@/utils/error-handling"
import { getCompanyActivitiesString } from "@/utils/mappings"
import ProgressSpinner from "@/components/ProgressSpinner"
import InfoTable from "./InfoTable.vue"
import DeclarationsTableSection from "@/components/NewBepiasViews/DeclarationsTableSection"

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
} = useFetch(() => `/api/v1/control/companies/${props.companyId}`, { immediate: false })
  .get()
  .json()

onMounted(async () => {
  await executeCompanyFetch()
  handleError(companyResponse)
})

const identityItems = computed(() => {
  if (!company.value) return []
  const c = company.value
  return [
    { title: "SIRET", body: [c.siret] }, // TODO: Include TVA
    { title: "No. téléphone", body: [c.phoneNumber] },
    { title: "Adresse siège", body: [c.address, `${c.postalCode}, ${c.city} ${c.country}`] },
    { title: "Rôles", body: [getCompanyActivitiesString(c.activities || []) || "Aucun rôle renseigné"] },
  ]
})

const insightsItems = computed(() => {
  if (!company.value) return []
  return [
    { title: "Nb. total de déclarations", body: ["TODO"] },
    { title: "Nb. de produits commercialisables", body: ["TODO"] },
  ]
})
</script>
