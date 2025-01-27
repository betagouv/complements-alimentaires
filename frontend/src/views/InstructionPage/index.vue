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
        <DsfrButton class="mt-2" label="Instruire" tertiary @click="instructDeclaration" />
      </DsfrAlert>
      <DeclarationAlert
        class="mb-6"
        v-else-if="!canInstruct && !declaration.declaredInTeleicare"
        role="instructor"
        :declaration="declaration"
        :snapshots="snapshots"
      />
      <DeclarationFromTeleicareAlert v-else-if="declaration.declaredInTeleicare" />
      <div v-if="declaration">
        <DeclarationSummary
          :showArticle="true"
          :useAccordions="true"
          :showElementAuthorization="true"
          :readonly="true"
          v-model="declaration"
          v-if="isAwaitingInstruction"
        />

        <DsfrTabs v-else v-model="selectedTabIndex" ref="tabs" :tab-titles="titles">
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
              :showArticle="true"
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
          <template v-slot:content v-if="!declaration.declaredInTeleicare">
            <h6 class="text-left">
              <v-icon name="ri-pencil-fill"></v-icon>
              Notes à destination de l'administration
            </h6>
            <div class="text-left mb-4 sm:mb-0 sm:flex sm:gap-8">
              <DsfrInputGroup>
                <DsfrInput
                  v-model="privateNotesInstruction"
                  is-textarea
                  label-visible
                  label="Notes de l'instruction"
                  @update:modelValue="saveComment"
                />
              </DsfrInputGroup>
              <DsfrInputGroup>
                <DsfrInput
                  :disabled="true"
                  v-model="privateNotesVisa"
                  is-textarea
                  label-visible
                  label="Notes du visa"
                />
              </DsfrInputGroup>
            </div>
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
import { useFetch, useDebounceFn } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import DeclarationSummary from "@/components/DeclarationSummary"
import IdentityTab from "@/components/IdentityTab"
import HistoryTab from "@/components/HistoryTab"
import DecisionTab from "./DecisionTab"
import { headers } from "@/utils/data-fetching"
import DeclarationAlert from "@/components/DeclarationAlert"
import { tabTitles } from "@/utils/mappings"
import { useRouter } from "vue-router"
import DeclarationFromTeleicareAlert from "@/components/DeclarationFromTeleicareAlert.vue"

const router = useRouter()
const previousRoute = router.getPreviousRoute()

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
} = useFetch(`/api/v1/declarations/${props.declarationId}`, { immediate: false }).get().json()
const privateNotesInstruction = ref(declaration.value?.privateNotesInstruction || "")
const privateNotesVisa = ref(declaration.value?.privateNotesVisa || "")
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

// Sauvegarde du commentaire privé
const saveComment = useDebounceFn(async () => {
  const { response } = await useFetch(() => `/api/v1/declarations/${declaration.value?.id}`, {
    headers: headers(),
  })
    .patch({ privateNotesInstruction: privateNotesInstruction.value })
    .json()
  handleError(response)
}, 600)

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)

  privateNotesInstruction.value = declaration.value?.privateNotesInstruction || ""
  privateNotesVisa.value = declaration.value?.privateNotesVisa || ""

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
  if (!declaration.value.declaredInTeleicare) baseComponents.push(HistoryTab)
  if (canInstruct.value) baseComponents.push(DecisionTab)
  return baseComponents
})
const titles = computed(() => tabTitles(components.value))
const selectedTabIndex = ref(0)

const instructDeclaration = async () => {
  const url = `/api/v1/declarations/${props.declarationId}/take-for-instruction/`
  const { response } = await useFetch(url, { headers: headers() }).post({}).json()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    await executeDeclarationFetch()
  }
}

const onDecisionDone = () => {
  const previousQuery = previousRoute.value.name === "InstructionDeclarations" ? previousRoute.value.query : {}
  router.push({ name: "InstructionDeclarations", query: previousQuery })
}
</script>

<style scoped>
div :deep(.fr-input-group) {
  @apply !mt-0;
  flex: 1;
}
</style>
