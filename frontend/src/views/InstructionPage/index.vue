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
      <DsfrAlert
        class="mb-4"
        v-if="isAwaitingInstruction && declaration.instructor?.id !== loggedUser.id"
        type="info"
        :title="
          declaration.instructor?.firstName
            ? `Cette déclaration est assignée à ${declaration.instructor.firstName} ${declaration.instructor.lastName}`
            : 'Cette déclaration n\'est pas encore assignée'
        "
      >
        <p>Vous pouvez vous assigner cette déclaration pour instruction</p>
        <DsfrButton
          class="mt-2"
          label="Instruire"
          tertiary
          @click="instructDeclaration"
          :disabled="isFetchingInstruction || isFetchingDeclaration"
        />
      </DsfrAlert>
      <DsfrAlert
        class="mb-4"
        v-else-if="declaration.instructor && declaration.instructor.id !== loggedUser.id"
        type="info"
        :title="`Cette déclaration est assignée à ${declaration.instructor.firstName} ${declaration.instructor.lastName}`"
      >
        <p>Vous pouvez vous assigner cette déclaration pour instruction</p>
        <DsfrButton class="mt-2" label="M'assigner cette déclaration" tertiary @click="assignInstruction" />
      </DsfrAlert>
      <DeclarationAlert
        class="mb-6"
        v-else-if="!canInstruct"
        role="instructor"
        :declaration="declaration"
        :snapshots="snapshots"
      />
      <DeclarationFromTeleicareAlert v-else-if="declaration.siccrfId" />
      <div v-if="declaration">
        <DeclarationSummary
          :allowArticleChange="!declaration.siccrfId"
          :useAccordions="true"
          :showElementAuthorization="true"
          :readonly="true"
          v-model="declaration"
          v-if="isAwaitingInstruction"
        />

        <DsfrTabs v-else v-model="selectedTabIndex" ref="tabs" :tab-titles="titles" @update:modelValue="selectTab">
          <DsfrTabContent
            v-for="(component, idx) in components"
            :key="`component-${idx}`"
            :panelId="`tab-content-${idx}`"
            :tabId="`tab-${idx}`"
          >
            <component
              :is="component"
              v-model="declaration"
              :externalResults="$externalResults"
              :readonly="true"
              :useAccordions="true"
              :showElementAuthorization="true"
              :declarationId="declaration?.id"
              :user="declarant"
              :company="company"
              :snapshots="snapshots"
              @decision-done="onDecisionDone"
              :allowArticleChange="!declaration.siccrfId"
              :useCompactAttachmentView="true"
            ></component>
          </DsfrTabContent>
        </DsfrTabs>
        <TabStepper
          v-if="!isAwaitingInstruction"
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
            <AdministrationNotes class="mb-4 sm:mb-0" v-model="declaration" :disableVisaNotes="true" />
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
import DecisionTab from "./DecisionTab"
import AdministrationNotes from "@/components/AdministrationNotes"
import { headers } from "@/utils/data-fetching"
import DeclarationAlert from "@/components/DeclarationAlert"
import { tabTitles } from "@/utils/mappings"
import { useRouter, useRoute } from "vue-router"
import DeclarationFromTeleicareAlert from "@/components/History/DeclarationFromTeleicareAlert.vue"
import useToaster from "@/composables/use-toaster"

const router = useRouter()
const route = useRoute()
const previousQueryParams =
  router.getPreviousRoute().value.name === "InstructionDeclarations" ? router.getPreviousRoute().value.query : {}

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
store.fetchDeclarationFieldsData()
const $externalResults = ref({})

const props = defineProps({
  declarationId: String,
})

const isAwaitingInstruction = computed(() => declaration.value?.status === "AWAITING_INSTRUCTION")
const canInstruct = computed(() => declaration.value?.status === "ONGOING_INSTRUCTION")

// Requêtes
const isFetching = ref(true)
const {
  response: declarationResponse,
  data: declaration,
  execute: executeDeclarationFetch,
  isFetching: isFetchingDeclaration,
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
  // AWAITING_INSTRUCTION, on la passe directement à ONGOING_INSTRUCTION.
  if (declaration.value?.instructor?.id === loggedUser.value.id && declaration.value.status === "AWAITING_INSTRUCTION")
    await instructDeclaration()

  await executeDeclarantFetch()
  handleError(declarantResponse)
  await executeCompanyFetch()
  handleError(companyResponse)
  await executeSnapshotsFetch()
  handleError(snapshotsResponse)
  isFetching.value = false
})

// Tab management
const components = computed(() => {
  const baseComponents = [IdentityTab, DeclarationSummary]
  if (!declaration.value.siccrfId) baseComponents.push(HistoryTab)
  if (canInstruct.value) baseComponents.push(DecisionTab)
  return baseComponents
})
const titles = computed(() => tabTitles(components.value))

const selectedTabIndex = ref(parseInt(route.query.tab))
const selectTab = async (index) => router.replace({ query: { tab: index } })

const assignInstruction = async () => {
  const url = `/api/v1/declarations/${props.declarationId}/assign-instruction/`
  const { response } = await useFetch(url, { headers: headers() }).post({}).json()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    await executeDeclarationFetch()
    useToaster().addSuccessMessage("La déclaration vous a été assignée")
  }
}

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

const instructDeclaration = async () => {
  await executeTakeForInstruction()
  $externalResults.value = await handleError(takeResponse)

  if (takeResponse.value.ok) {
    await executeDeclarationFetch()
  }
}

const onDecisionDone = () => {
  router.push({ name: "InstructionDeclarations", query: previousQueryParams })
}
</script>

<style scoped>
@reference "../../styles/index.css";

div :deep(.fr-input-group) {
  @apply mt-0!;
  flex: 1;
}
</style>
