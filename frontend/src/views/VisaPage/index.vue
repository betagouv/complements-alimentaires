<template>
  <div class="fr-container mb-10">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: { name: 'VisaDeclarations' }, text: 'Déclarations pour visa / signature' },
        { text: 'Visa' },
      ]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else>
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
      <div v-if="declaration">
        <DeclarationSummary
          :allowArticleChange="!declaration.siccrfId"
          :useAccordions="true"
          :showElementAuthorization="true"
          :readonly="true"
          v-model="declaration"
          v-if="isAwaitingVisa"
        />

        <DsfrTabs v-else ref="tabs" :tab-titles="titles" v-model="selectedTabIndex">
          <DsfrTabContent
            v-for="(component, idx) in components"
            :key="`component-${idx}`"
            :panelId="`tab-content-${idx}`"
            :tabId="`tab-${idx}`"
          >
            <component
              :is="component"
              :allowArticleChange="!declaration.siccrfId"
              v-model="declaration"
              :externalResults="$externalResults"
              :readonly="true"
              :declarationId="declaration?.id"
              :useAccordions="true"
              :showElementAuthorization="true"
              :user="declarant"
              :company="company"
              :mandatedCompany="mandatedCompany"
              :snapshots="snapshots"
              :useCompactAttachmentView="true"
              @decision-done="onDecisionDone"
            ></component>
          </DsfrTabContent>
        </DsfrTabs>
        <TabStepper
          v-if="!isAwaitingVisa"
          :titles="titles"
          :selectedTabIndex="selectedTabIndex"
          @back="selectedTabIndex -= 1"
          @forward="selectedTabIndex += 1"
          :removeSaveLabel="true"
        >
          <template v-slot:content v-if="!declaration.siccrfId">
            <h6 class="text-left">
              <v-icon name="ri-pencil-fill"></v-icon>
              Notes à destination de l'administration
            </h6>
            <AdministrationNotes class="mb-4 sm:mb-0" v-model="declaration" :disableInstructionNotes="true" />
          </template>
        </TabStepper>
      </div>
    </div>
  </div>
</template>

<script setup>
import TabStepper from "@/components/TabStepper"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { onMounted, computed, ref } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import DeclarationSummary from "@/components/DeclarationSummary"
import IdentityTab from "@/components/IdentityTab"
import HistoryTab from "@/components/HistoryTab"
import DeclarationAlert from "@/components/DeclarationAlert"
import VisaValidationTab from "./VisaValidationTab"
import AdministrationNotes from "@/components/AdministrationNotes"
import { headers } from "@/utils/data-fetching"
import { tabTitles } from "@/utils/mappings"
import { useRouter } from "vue-router"

const router = useRouter()
const previousRoute = router.getPreviousRoute()

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
store.fetchDeclarationFieldsData()
const $externalResults = ref({})

const props = defineProps({
  declarationId: String,
})

const isAwaitingVisa = computed(() => declaration.value?.status === "AWAITING_VISA")
const canInstruct = computed(() => declaration.value?.status === "ONGOING_VISA")

// Requêtes
const isFetching = ref(true)
const {
  response: declarationResponse,
  data: declaration,
  execute: executeDeclarationFetch,
} = useFetch(`/api/v1/declarations/${props.declarationId}`, { immediate: false }).get().json()

const {
  response: declarantResponse,
  data: declarant,
  execute: executeDeclarantFetch,
} = useFetch(() => `/api/v1/users/${declaration.value?.author}`, { immediate: false })
  .get()
  .json()

const {
  response: companyResponse,
  data: company,
  execute: executeCompanyFetch,
} = useFetch(() => `/api/v1/companies/${declaration.value?.company}`, { immediate: false })
  .get()
  .json()

const {
  response: mandatedCompanyResponse,
  data: mandatedCompany,
  execute: executeMandatedCompanyFetch,
} = useFetch(() => `/api/v1/companies/${declaration.value?.mandatedCompany}`, { immediate: false })
  .get()
  .json()

const {
  response: snapshotsResponse,
  data: snapshots,
  execute: executeSnapshotsFetch,
} = useFetch(() => `/api/v1/declarations/${props.declarationId}/snapshots/`, { immediate: false })
  .get()
  .json()

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)

  // Si on arrive à cette page avec une déclaration déjà assignée à quelqun.e mais en état
  // AWAITING_VISA, on la passe directement à ONGOING_VISA.
  if (declaration.value?.visor?.id === loggedUser.value.id && declaration.value.status === "AWAITING_VISA")
    await takeDeclaration()

  await executeDeclarantFetch()
  handleError(declarantResponse)
  await executeCompanyFetch()
  handleError(companyResponse)

  if (declaration.value?.mandatedCompany) {
    await executeMandatedCompanyFetch()
    handleError(mandatedCompanyResponse)
  }

  await executeSnapshotsFetch()
  handleError(snapshotsResponse)
  isFetching.value = false
})

// Tab management
const components = computed(() => {
  const baseComponents = [IdentityTab, DeclarationSummary]
  if (!declaration.value.siccrfId) baseComponents.push(HistoryTab)
  if (canInstruct.value) baseComponents.push(VisaValidationTab)
  return baseComponents
})
const titles = computed(() => tabTitles(components.value))
const selectedTabIndex = ref(0)

const takeDeclaration = async () => {
  const url = `/api/v1/declarations/${props.declarationId}/take-for-visa/`
  const { response } = await useFetch(url, { headers: headers() }).post({}).json()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    await executeDeclarationFetch()
  }
}

const onDecisionDone = () => {
  const previousQuery = previousRoute.value.name === "VisaDeclarations" ? previousRoute.value.query : {}
  router.push({ name: "VisaDeclarations", query: previousQuery })
}
</script>

<style scoped>
@reference "../../styles/index.css";
div :deep(.fr-input-group) {
  @apply mt-0!;
  flex: 1;
}
</style>
