<template>
  <div class="fr-container mb-10">
    <CaBreadcrumb :links="breadcrumbs" />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="declaration">
      <div class="flex gap-10 items-center">
        <h1 class="mb-0">{{ declaration.name }}</h1>
        <div>
          <DsfrBadge type="warning" label="Article inconnu" v-if="!declaration.article" />
          <DsfrBadge
            no-icon
            v-else
            :label="articleOptionsWith15Subtypes.find((x) => x.value === declaration.article)?.text"
          />
        </div>
      </div>

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
            :snapshots="snapshots"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router"
import { articleOptionsWith15Subtypes } from "@/utils/mappings"
import { computed, onMounted, watch } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import CaBreadcrumb from "@/components/CaBreadcrumb"
import NavSidebar from "./NavSidebar"
import { useRootStore } from "@/stores/root"
import { setDocumentTitle } from "@/utils/document"

const store = useRootStore()
store.fetchDeclarationFieldsData()

const route = useRoute()
const router = useRouter()

const breadcrumbs = computed(() => {
  const routes = [{ to: { name: "DashboardPage" }, text: "Tableau de bord" }]
  if (router.getPreviousRoute().value?.name === "CompanyDetails") {
    routes.push({ to: { name: "CompanySearchPage" }, text: "Recherche entreprises" })
    routes.push(
      company.value
        ? {
            to: { name: "CompanyDetails", params: { companyId: company.value.id } },
            text: company.value.socialName || "Entreprise",
          }
        : { text: "Entreprise" }
    )
  } else {
    routes.push({ to: { name: "DeclarationSearchPage" }, text: "Recherche compléments alimentaires" })
  }

  routes.push({ text: declaration.value?.name || "Complément alimentaire" })

  return routes
})

const props = defineProps({ declarationId: String })
const makeRequest = (url) => useFetch(url, { immediate: false }).get().json()

const isFetching = computed(() =>
  [isFetchingDeclaration, isFetchingDeclarant, isFetchingCompany, isFetchingMandatedCompany, isFetchingSnapshots].some(
    (x) => !!x.value
  )
)

const {
  response: declarationResponse,
  data: declaration,
  execute: executeDeclarationFetch,
  isFetching: isFetchingDeclaration,
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

const {
  response: snapshotsResponse,
  data: snapshots,
  execute: executeSnapshotsFetch,
  isFetching: isFetchingSnapshots,
} = makeRequest(() => `/api/v1/declarations/${props.declarationId}/snapshots/`)
  .get()
  .json()

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)

  if (!declaration.value) return

  const mandatedCompany = declaration.value.mandatedCompany
  const fetchMandatedCompany = mandatedCompany ? executeMandatedCompanyFetch : () => Promise.resolve
  const handleMandatedError = mandatedCompany ? () => handleError(mandatedCompanyResponse) : () => Promise.resolve

  // L'historique n'est visible que lors que la déclaration es refusée ou abandonnée
  const showHistory = declaration.value.status === "REJECTED" || declaration.value.status === "ABANDONED"
  const fetchSnapshots = showHistory ? executeSnapshotsFetch : () => Promise.resolve
  const handleSnapshotsError = showHistory ? () => handleError(snapshotsResponse) : () => Promise.resolve

  await Promise.all([executeDeclarantFetch(), executeCompanyFetch(), fetchMandatedCompany(), fetchSnapshots()])
  await Promise.all([
    handleError(declarantResponse),
    handleError(companyResponse),
    handleMandatedError(),
    handleSnapshotsError(),
  ])

  if (route.hash) {
    // La fonction scrollBehavior du router est lancée avant le rendu asynchrone de cette
    // vue, donc on doit vérifier s'il y a un ancrage dans l'URL pour scroller dessus
    const el = document.querySelector(route.hash)
    if (el) el.scrollIntoView({ behavior: "smooth" })
  }

  setDocumentTitleFromRoute()
})

const setDocumentTitleFromRoute = () => {
  const companyName = company.value.socialName || "Résultat entreprise"
  if (route.name.includes("History")) setDocumentTitle(["Historique", declaration.value.name, companyName])
  else if (route.name.includes("Identity"))
    setDocumentTitle(["Identité produit et entreprise", declaration.value.name, companyName])
  else setDocumentTitle([declaration.value.name, companyName])
}

watch(route, setDocumentTitleFromRoute)
</script>
