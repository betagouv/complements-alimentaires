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
    <div v-else>
      <DsfrAlert type="warning" title="Cette interface est en construction" class="mb-4" />
      <h1 v-if="declaration">{{ declaration.name }}</h1>
      <div class="sm:grid sm:grid-cols-12 sm:gap-4">
        <div class="hidden sm:block col-span-3">
          <div class="sticky top-2 sidebar-content">
            <InstructionSidebar />
          </div>
        </div>
        <div class="col-span-12 sm:col-span-9 h-lvh">Colonne à droite</div>
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
import ProgressSpinner from "@/components/ProgressSpinner"
import InstructionSidebar from "./InstructionSidebar"

const props = defineProps({ declarationId: String })

const isFetching = computed(() =>
  [isFetchingDeclaration, isFetchingDeclarant, isFetchingCompany, isFetchingSnapshots].some((x) => !!x.value)
)

const privateNotesInstruction = computed(() => declaration.value?.privateNotesInstruction || "")
const privateNotesVisa = computed(() => declaration.value?.privateNotesVisa || "")

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

  privateNotesInstruction.value = declaration.value?.privateNotesInstruction || ""
  privateNotesVisa.value = declaration.value?.privateNotesVisa || ""

  // Si on arrive à cette page avec une déclaration déjà assignée à quelqun.e mais en état
  // AWAITING_INSTRUCTION, on la passe directement à ONGOING_INSTRUCTION.
  // TODO
  // if (declaration.value?.instructor?.id === loggedUser.value.id && declaration.value.status === "AWAITING_INSTRUCTION")
  //   await instructDeclaration()

  // TODO gestion d'erreur
  if (declaration.value) await Promise.all([executeDeclarantFetch(), executeCompanyFetch(), executeSnapshotsFetch()])
})
</script>
