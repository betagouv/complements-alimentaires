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
        <DsfrButton class="mt-2" label="Valider" tertiary @click="validateDeclaration" />
      </DsfrAlert>
      <DeclarationAlert class="mb-4" v-else-if="!canInstruct" :status="declaration.status" />
      <div v-if="declaration">
        <DeclarationSummary :readonly="true" v-model="declaration" v-if="isAwaitingVisa" />

        <DsfrTabs v-else ref="tabs" :tab-titles="tabTitles" :initialSelectedIndex="0" @select-tab="selectTab">
          <DsfrTabContent panelId="tab-content-0" tabId="tab-0" :selected="selectedTabIndex === 0" :asc="asc">
            <IdentityTab :user="declarant" :company="company" />
          </DsfrTabContent>
          <DsfrTabContent panelId="tab-content-1" tabId="tab-1" :selected="selectedTabIndex === 1" :asc="asc">
            <DeclarationSummary :readonly="true" v-model="declaration" />
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
            Valider cette déclaration
          </DsfrTabContent>
        </DsfrTabs>
      </div>
    </div>
  </div>
</template>

<script setup>
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

const store = useRootStore()
const { loggedUser } = storeToRefs(store)
store.fetchDeclarationFieldsData()
const tabs = ref(null) // Corresponds to the template ref (https://vuejs.org/guide/essentials/template-refs.html#accessing-the-refs)

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

onMounted(async () => {
  await executeDeclarationFetch()
  handleError(declarationResponse)

  // Si on arrive à cette page avec une déclaration déjà assignée à quelqun.e mais en état
  // AWAITING_VISA, on la passe directement à ONGOING_VISA.
  if (declaration.value?.visor?.id === loggedUser.value.id && declaration.value.status === "AWAITING_VISA")
    await validateDeclaration()

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
    tabs.push({ title: "Visa / Signature", icon: "ri-checkbox-circle-line", tabId: "tab-3", panelId: "tab-content-3" })
  return tabs
})
const selectedTabIndex = ref(0)
const asc = ref(true) // Je n'aime pas le nommage mais ça vient de ce paramètre : https://vue-dsfr.netlify.app/?path=/docs/composants-dsfrtabs--docs
const selectTab = (index) => {
  asc.value = selectedTabIndex.value < index
  selectedTabIndex.value = index
}

const validateDeclaration = async () => {
  console.log("Take for validation")
}
</script>
