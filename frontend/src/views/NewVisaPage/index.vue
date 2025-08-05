<template>
  <div class="fr-container mb-10">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: { name: 'VisaDeclarations' }, text: 'Déclarations pour visa' },
        { text: 'Visa' },
      ]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="declaration">
      <h1>{{ declaration.name }}</h1>
      <DsfrAlert
        class="mb-4"
        v-if="isAwaitingVisa && !declaration.visa"
        type="info"
        title="Cette déclaration n'est pas encore assignée pour validation"
      >
        <p>Vous pouvez vous assigner cette déclaration pour visa / signature</p>
        <DsfrButton class="mt-2" label="Prendre pour validation" tertiary @click="takeDeclaration" />
      </DsfrAlert>
      <DeclarationAlert role="visor" class="mb-4" :declaration="declaration" :snapshots="snapshots" />
      <DeclarationSummary
        :allowArticleChange="!declaration.siccrfId"
        :useAccordions="true"
        :showElementAuthorization="true"
        :readonly="true"
        v-model="declaration"
        v-if="isAwaitingVisa"
      />

      <div v-else class="sm:grid sm:grid-cols-12">
        <div class="hidden sm:block col-span-3">
          <div class="sticky top-2 sidebar-content">
            <BepiasSidebar v-model="declaration" role="visa" />
          </div>
        </div>
        <div class="col-span-12 sm:col-span-9 bg-grey-975!">
          <router-view
            :declaration="declaration"
            :declarant="declarant"
            :company="company"
            :mandatedCompany="mandatedCompany"
            :snapshots="snapshots"
            role="visa"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { useRoute } from "vue-router"
import { headers } from "@/utils/data-fetching"
import ProgressSpinner from "@/components/ProgressSpinner"
import BepiasSidebar from "@/components/NewBepiasViews/BepiasSidebar"
import DeclarationSummary from "@/components/DeclarationSummary"
import DeclarationAlert from "@/components/DeclarationAlert"

const props = defineProps({ declarationId: String })
const route = useRoute()

const isFetching = computed(() =>
  [
    isFetchingDeclaration,
    isFetchingDeclarant,
    isFetchingCompany,
    isFetchingMandatedCompany,
    isFetchingSnapshots,
    isFetchingVisa,
  ].some((x) => !!x.value)
)

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
store.fetchDeclarationFieldsData()

// Requêtes
const makeRequest = (url) => useFetch(url, { immediate: false }).get().json()
const {
  response: declarationResponse,
  data: declaration,
  execute: executeDeclarationFetch,
  isFetching: isFetchingDeclaration,
} = makeRequest(`/api/v1/declarations/${props.declarationId}`)

const {
  response: declarantResponse,
  data: declarant,
  execute: executeDeclarantFetch,
  isFetching: isFetchingDeclarant,
} = makeRequest(() => `/api/v1/users/${declaration.value?.author}`)
  .get()
  .json()
const {
  response: companyResponse,
  data: company,
  execute: executeCompanyFetch,
  isFetching: isFetchingCompany,
} = makeRequest(() => `/api/v1/companies/${declaration.value?.company}`)
  .get()
  .json()
const {
  response: mandatedCompanyResponse,
  data: mandatedCompany,
  execute: executeMandatedCompanyFetch,
  isFetching: isFetchingMandatedCompany,
} = makeRequest(() => `/api/v1/companies/${declaration.value?.mandatedCompany}`)
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

const {
  response: takeResponse,
  execute: executeTakeForVisa,
  isFetching: isFetchingVisa,
} = useFetch(
  `/api/v1/declarations/${props.declarationId}/take-for-visa/`,
  {
    headers: headers(),
  },
  { immediate: false }
)
  .post({})
  .json()

const takeDeclaration = async () => {
  await executeTakeForVisa()
  await handleError(takeResponse)

  if (takeResponse.value.ok) {
    await executeDeclarationFetch()
  }
}

const isAwaitingVisa = computed(() => declaration.value?.status === "AWAITING_VISA")

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)

  if (!declaration.value) return

  // Si on arrive à cette page avec une déclaration déjà assignée à l'utilisateur·ice mais en état
  // AWAITING_VISA, on la passe directement à ONGOING_VISA.
  if (declaration.value.visor?.id === loggedUser.value.id && declaration.value.status === "AWAITING_VISA")
    await takeDeclaration()

  const mandatedCompany = declaration.value.mandatedCompany
  const fetchMandatedCompany = mandatedCompany ? executeMandatedCompanyFetch : () => Promise.resolve
  const handleMandatedError = mandatedCompany ? () => handleError(mandatedCompanyResponse) : () => Promise.resolve

  await Promise.all([executeDeclarantFetch(), executeCompanyFetch(), fetchMandatedCompany(), executeSnapshotsFetch()])
  await Promise.all([
    handleError(declarantResponse),
    handleError(companyResponse),
    handleMandatedError(),
    handleError(snapshotsResponse),
  ])

  if (route.hash) {
    // La fonction scrollBehavior du router est lancée avant le rendu asynchrone de cette
    // vue, donc on doit vérifier s'il y a un ancrage dans l'URL pour scroller dessus
    const el = document.querySelector(route.hash)
    if (el) el.scrollIntoView({ behavior: "smooth" })
  }
})
</script>
