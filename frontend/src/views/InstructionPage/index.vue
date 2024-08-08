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
        v-if="isAwaitingInstruction && declaration.instructor.id !== loggedUser.id"
        type="info"
        :title="
          declaration.instructor && declaration.instructor.firstName
            ? `Cette déclaration est assignée à ${declaration.instructor.firstName} ${declaration.instructor.lastName}`
            : 'Cette déclaration n\'est pas encore assignée'
        "
      >
        <p>Vous pouvez vous assigner cette déclaration pour instruction</p>
        <DsfrButton class="mt-2" label="Instruire" tertiary @click="instructDeclaration" />
      </DsfrAlert>
      <DeclarationAlert class="mb-6" v-else-if="!canInstruct" role="instructor" :declaration="declaration" />
      <div v-if="declaration">
        <DeclarationSummary :readonly="true" v-model="declaration" v-if="isAwaitingInstruction" />

        <DsfrTabs v-else ref="tabs" :tab-titles="titles" :initialSelectedIndex="0" @select-tab="selectTab">
          <DsfrTabContent
            v-for="(component, idx) in components"
            :key="`component-${idx}`"
            :panelId="`tab-content-${idx}`"
            :tabId="`tab-${idx}`"
            :selected="selectedTabIndex === idx"
            :asc="asc"
          >
            <component
              :is="component"
              v-model="declaration"
              :externalResults="$externalResults"
              :readonly="true"
              :declarationId="declaration?.id"
              :privateNotes="declaration?.privateNotes"
              :user="declarant"
              :company="company"
              @decision-done="onDecisionDone"
            ></component>
          </DsfrTabContent>
        </DsfrTabs>
        <TabStepper
          v-if="!isAwaitingInstruction"
          :titles="titles"
          :selectedTabIndex="selectedTabIndex"
          @back="selectTab(selectedTabIndex - 1)"
          @forward="selectTab(selectedTabIndex + 1)"
        />
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
import { headers } from "@/utils/data-fetching"
import DeclarationAlert from "@/components/DeclarationAlert"
import { tabTitles } from "@/utils/mappings"
import { useRouter } from "vue-router"

const router = useRouter()
const previousRoute = router.getPreviousRoute()

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
store.fetchDeclarationFieldsData()
const $externalResults = ref({})
const tabs = ref(null) // Corresponds to the template ref (https://vuejs.org/guide/essentials/template-refs.html#accessing-the-refs)

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
  isFetching.value = false
})

// Tab management
const components = computed(() => {
  const baseComponents = [DeclarationSummary, HistoryTab]
  if (canInstruct.value) baseComponents.push(DecisionTab)
  baseComponents.push(IdentityTab)
  return baseComponents
})
const titles = computed(() => tabTitles(components.value))
const selectedTabIndex = ref(0)
const asc = ref(true) // Je n'aime pas le nommage mais ça vient de ce paramètre : https://vue-dsfr.netlify.app/?path=/docs/composants-dsfrtabs--docs
const selectTab = (index) => {
  if (index === selectedTabIndex.value) return
  asc.value = selectedTabIndex.value < index
  selectedTabIndex.value = index
  tabs.value?.selectIndex?.(selectedTabIndex.value)
}

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
