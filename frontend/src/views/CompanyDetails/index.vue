<template>
  <div class="fr-container mb-10">
    <CaBreadcrumb
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
          <h2 class="fr-h4">Identité entreprise</h2>
          <InfoTable :items="identityItems" />
        </div>
        <div class="col-span-2 sm:col-span-1">
          <h2 class="fr-h4">Chiffres clés</h2>
          <InfoTable :items="insightsItems" />
        </div>
      </div>
      <div v-if="company.totalDeclarations > 0">
        <h2 class="mt-8 fr-h4">Produits déclarés auprès de la DGAL par cette entreprise</h2>
        <DeclarationsTableSection :companyId="companyId" />
      </div>
      <p class="mt-8 italic" v-else>Il n'y a pas de produits déclarés auprès de la DGAL par cette entreprise.</p>
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
import InfoTable from "@/components/InfoTable.vue"
import DeclarationsTableSection from "@/components/NewBepiasViews/DeclarationsTableSection"
import CaBreadcrumb from "@/components/CaBreadcrumb"
import { setDocumentTitle } from "@/utils/document"
import { useRootStore } from "@/stores/root"

useRootStore().fetchDeclarationFieldsData()
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
  setDocumentTitle([company.value?.socialName, "Détail de l'entreprise"])
})

const identityItems = computed(() => {
  if (!company.value) return []
  const c = company.value
  const firstLine = c.siret ? { title: "SIRET", body: [c.siret] } : { title: "No. de TVA", body: [c.vat] }
  return [
    firstLine,
    { title: "No. téléphone", body: [c.phoneNumber] },
    { title: "Adresse siège", body: [c.address, `${c.postalCode}, ${c.city} ${c.country}`] },
    { title: "Rôles", body: [getCompanyActivitiesString(c.activities || []) || "Aucun rôle renseigné"] },
  ]
})

const insightsItems = computed(() => {
  if (!company.value) return []
  const c = company.value
  return [
    { title: "Nb. total de déclarations", body: [c.totalDeclarations] },
    { title: "Nb. de produits commercialisables", body: [c.marketReadyDeclarations] },
    { title: "Nb. de produits en cours d'instruction", body: [c.ongoingDeclarations] },
    { title: "Nb. de produits refusés", body: [c.refusedDeclarations] },
    { title: "Nb. de produits retirés du marché", body: [c.withdrawnDeclarations] },
    { title: "Nb. de produits en instruction interrompue", body: [c.interruptedDeclarations] },
  ]
})
</script>
