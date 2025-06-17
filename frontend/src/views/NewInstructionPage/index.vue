<template>
  <div class="fr-container mb-10">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: { name: 'InstructionDeclarations' }, text: 'Déclarations pour instruction' },
        { text: 'Instruction' },
      ]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else-if="declaration">
      <h1>{{ declaration.name }}</h1>
      <AlertsSection
        v-model="declaration"
        @instruct="instructDeclaration"
        @assign="assignToSelf"
        :snapshots="snapshots"
      />
      <DeclarationSummary
        :allowArticleChange="!declaration.siccrfId"
        :useAccordions="true"
        :showElementAuthorization="true"
        :readonly="true"
        v-model="declaration"
        v-if="isAwaitingInstruction"
      />

      <div v-else class="sm:grid sm:grid-cols-12">
        <div class="hidden sm:block col-span-3">
          <div class="sticky top-2 sidebar-content">
            <InstructionSidebar v-model="declaration" />
          </div>
        </div>
        <div class="col-span-12 sm:col-span-9">
          <router-view :declaration="declaration" :declarant="declarant" :company="company" :snapshots="snapshots" />
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
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import ProgressSpinner from "@/components/ProgressSpinner"
import InstructionSidebar from "./InstructionSidebar"
import AlertsSection from "@/components/AlertsSection"
import DeclarationSummary from "@/components/DeclarationSummary"

const props = defineProps({ declarationId: String })

const isFetching = computed(() =>
  [
    isFetchingDeclaration,
    isFetchingDeclarant,
    isFetchingCompany,
    isFetchingSnapshots,
    isFetchingInstruction,
    isFetchingAssignToSelf,
  ].some((x) => !!x.value)
)

// Note : à utiliser dans les text-areas en bas de l'écran
// const privateNotesInstruction = computed(() => declaration.value?.privateNotesInstruction || "")
// const privateNotesVisa = computed(() => declaration.value?.privateNotesVisa || "")

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
  // response: declarantResponse,
  data: declarant,
  execute: executeDeclarantFetch,
  isFetching: isFetchingDeclarant,
} = makeRequest(() => `/api/v1/users/${declaration.value?.author}`)
  .get()
  .json()
const {
  // response: companyResponse,
  data: company,
  execute: executeCompanyFetch,
  isFetching: isFetchingCompany,
} = makeRequest(() => `/api/v1/companies/${declaration.value?.company}`)
  .get()
  .json()
const {
  // response: snapshotsResponse,
  data: snapshots,
  execute: executeSnapshotsFetch,
  isFetching: isFetchingSnapshots,
} = makeRequest(() => `/api/v1/declarations/${props.declarationId}/snapshots/`)
  .get()
  .json()

const {
  response: takeResponse,
  execute: executeTakeForInstruction,
  isFetching: isFetchingInstruction,
} = useFetch(
  `/api/v1/declarations/${props.declarationId}/take-for-instruction/`,
  {
    headers: headers(),
  },
  { immediate: false }
)
  .post({})
  .json()

const {
  response: assignResponse,
  execute: executeAssignToSelf,
  isFetching: isFetchingAssignToSelf,
} = useFetch(
  `/api/v1/declarations/${props.declarationId}/assign-instruction/`,
  {
    headers: headers(),
  },
  { immediate: false }
)
  .post({})
  .json()

const instructDeclaration = async () => {
  await executeTakeForInstruction()
  // $externalResults.value = await handleError(takeResponse)

  if (takeResponse.value.ok) {
    await executeDeclarationFetch()
  }
}

const assignToSelf = async () => {
  await executeAssignToSelf()
  // $externalResults.value = await handleError(response)

  if (assignResponse.value.ok) {
    await executeDeclarationFetch()
    useToaster().addSuccessMessage("La déclaration vous a été assignée")
  }
}

const isAwaitingInstruction = computed(() => declaration.value?.status === "AWAITING_INSTRUCTION")

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)

  // Si on arrive à cette page avec une déclaration déjà assignée à quelqun.e mais en état
  // AWAITING_INSTRUCTION, on la passe directement à ONGOING_INSTRUCTION.
  // TODO gestion d'erreur
  if (declaration.value?.instructor?.id === loggedUser.value.id && declaration.value.status === "AWAITING_INSTRUCTION")
    await instructDeclaration()

  // TODO gestion d'erreur
  if (declaration.value) await Promise.all([executeDeclarantFetch(), executeCompanyFetch(), executeSnapshotsFetch()])
})
</script>
