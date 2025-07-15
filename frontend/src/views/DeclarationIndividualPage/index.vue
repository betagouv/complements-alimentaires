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
      <h1 class="mb-0">{{ declaration.name }}</h1>

      <div class="sm:grid sm:grid-cols-12">
        <div class="hidden sm:block col-span-3">
          <div class="sticky top-2 sidebar-content">
            <NavSidebar v-model="declaration" />
          </div>
        </div>
        <div class="col-span-12 sm:col-span-9">
          <router-view
            :declaration="declaration"
            :declarant="declarant"
            :company="company"
            :mandatedCompany="mandatedCompany"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from "vue-router"
import { computed, onMounted } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import NavSidebar from "./NavSidebar"

const router = useRouter()
const route = useRoute()
const previousRoute = computed(() => {
  const previousRoute = router.getPreviousRoute().value
  return previousRoute?.name === "CompanySearchPage" ? previousRoute : { name: "CompanySearchPage" }
})

const props = defineProps({ declarationId: String })
const makeRequest = (url) => useFetch(url, { immediate: false }).get().json()

const {
  response: declarationResponse,
  data: declaration,
  execute: executeDeclarationFetch,
  isFetching,
} = makeRequest(`/api/v1/control/declarations/${props.declarationId}`).get().json()

const {
  response: declarantResponse,
  data: declarant,
  execute: executeDeclarantFetch,
  isFetching: isFetchingDeclarant,
} = makeRequest(() => `/api/v1/control/users/${declaration.value?.author}`)
  .get()
  .json()
const {
  response: companyResponse,
  data: company,
  execute: executeCompanyFetch,
  isFetching: isFetchingCompany,
} = makeRequest(() => `/api/v1/control/companies/${declaration.value?.company}`)
  .get()
  .json()

const {
  response: mandatedCompanyResponse,
  data: mandatedCompany,
  execute: executeMandatedCompanyFetch,
  isFetching: isFetchingMandatedCompany,
} = makeRequest(() => `/api/v1/control/companies/${declaration.value?.mandatedCompany}`)
  .get()
  .json()

// const {
//   response: snapshotsResponse,
//   data: snapshots,
//   execute: executeSnapshotsFetch,
//   isFetching: isFetchingSnapshots,
// } = makeRequest(() => `/api/v1/declarations/${props.declarationId}/snapshots/`)
//   .get()
//   .json()

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)

  if (!declaration.value) return

  const mandatedCompany = declaration.value.mandatedCompany
  const fetchMandatedCompany = mandatedCompany ? executeMandatedCompanyFetch : () => Promise.resolve
  const handleMandatedError = mandatedCompany ? () => handleError(mandatedCompanyResponse) : () => Promise.resolve

  await Promise.all([executeDeclarantFetch(), executeCompanyFetch(), fetchMandatedCompany()])
  await Promise.all([handleError(declarantResponse), handleError(companyResponse), handleMandatedError()])

  if (route.hash) {
    // La fonction scrollBehavior du router est lancée avant le rendu asynchrone de cette
    // vue, donc on doit vérifier s'il y a un ancrage dans l'URL pour scroller dessus
    const el = document.querySelector(route.hash)
    if (el) el.scrollIntoView({ behavior: "smooth" })
  }
})
</script>
