<template>
  <div class="fr-container mb-10">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[
        { to: { name: 'DashboardPage' }, text: 'Tableau de bord' },
        { to: { name: 'InstructionDeclarations' }, text: 'Instruction' },
        { text: 'Instruction' },
      ]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else>
      <DsfrAlert
        class="mb-4"
        v-if="isAwaitingInstruction && !declaration.instructor"
        type="info"
        title="Cette déclaration n'est pas encore assignée"
      >
        <p>Vous pouvez vous assigner cette déclaration pour instruction</p>
        <DsfrButton class="mt-2" label="Instruire" tertiary @click="instructDeclaration" />
      </DsfrAlert>
      <DsfrAlert
        class="mb-4"
        v-else-if="!canInstruct"
        :type="declaration.status === 'AUTHORIZED' ? 'success' : 'info'"
        :title="`Cette déclaration est en status « ${statusProps[declaration.status].label} »`"
      />
      <div v-if="declaration">
        <SummaryTab v-model="declaration" v-if="isAwaitingInstruction" />

        <DsfrTabs v-else ref="tabs" :tab-titles="tabTitles" :initialSelectedIndex="0" @select-tab="selectTab">
          <DsfrTabContent panelId="tab-content-0" tabId="tab-0" :selected="selectedTabIndex === 0" :asc="asc">
            <IdentityTab :user="declarant" :company="company" />
          </DsfrTabContent>
          <DsfrTabContent panelId="tab-content-1" tabId="tab-1" :selected="selectedTabIndex === 1" :asc="asc">
            <SummaryTab v-model="declaration" />
          </DsfrTabContent>
          <DsfrTabContent panelId="tab-content-2" tabId="tab-2" :selected="selectedTabIndex === 2" :asc="asc">
            <HistoryTab :declarationId="declaration?.id" />
          </DsfrTabContent>
          <DsfrTabContent
            v-if="canInstruct"
            panelId="tab-content-3"
            tabId="tab-3"
            :selected="selectedTabIndex === 3"
            :asc="asc"
          >
            <DecisionTab :declarationId="declaration?.id" @reload-declaration="reloadDeclaration" />
          </DsfrTabContent>
        </DsfrTabs>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { onMounted, computed, ref, nextTick } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import SummaryTab from "./SummaryTab"
import IdentityTab from "./IdentityTab"
import HistoryTab from "./HistoryTab"
import DecisionTab from "./DecisionTab"
import { headers } from "@/utils/data-fetching"
import { statusProps } from "@/utils/mappings"

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
const tabTitles = computed(() => {
  const tabs = [
    { title: "Identité", icon: "ri-shield-user-line", tabId: "tab-0", panelId: "tab-content-0" },
    { title: "Le produit", icon: "ri-flask-line", tabId: "tab-1", panelId: "tab-content-1" },
    { title: "Historique", icon: "ri-chat-3-line", tabId: "tab-2", panelId: "tab-content-2" },
  ]
  if (canInstruct.value)
    tabs.push({ title: "Décision", icon: "ri-checkbox-circle-line", tabId: "tab-3", panelId: "tab-content-3" })
  return tabs
})
const selectedTabIndex = ref(0)
const asc = ref(true) // Je n'aime pas le nommage mais ça vient de ce paramètre : https://vue-dsfr.netlify.app/?path=/docs/composants-dsfrtabs--docs
const selectTab = (index) => {
  asc.value = selectedTabIndex.value < index
  selectedTabIndex.value = index
}

const instructDeclaration = async () => {
  const url = `/api/v1/declarations/${props.declarationId}/take-for-instruction/`
  const { response } = await useFetch(url, { headers: headers() }).post({}).json()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    await executeDeclarationFetch()
  }
}

const reloadDeclaration = async () => {
  tabs.value?.selectIndex?.(0)
  await nextTick()
  await executeDeclarationFetch()
}
</script>
