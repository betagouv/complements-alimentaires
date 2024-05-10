<template>
  <div class="fr-container mb-10">
    <DsfrBreadcrumb
      class="mb-8"
      :links="[
        { to: '/tableau-de-bord', text: 'Tableau de bord' },
        { to: '/toutes-les-declarations', text: 'Toutes les déclarations' },
        { text: 'Instruction' },
      ]"
    />
    <div v-if="isFetching" class="flex justify-center my-10">
      <ProgressSpinner />
    </div>
    <div v-else>
      <DsfrAlert v-if="isDraft" type="warning" title="Cette déclaration n'est pas encore prête pour instruction">
        <p>La déclaration est en mode brouillon et peut encore être modifié par l'utilisateur.</p>
        <DsfrButton
          class="mt-2"
          label="Retour à la liste de déclarations"
          tertiary
          @click="$router.push({ name: 'AllDeclarations' })"
        />
      </DsfrAlert>
      <DsfrTabs v-if="declaration" ref="tabs" :tab-titles="tabTitles" :initialSelectedIndex="0" @select-tab="selectTab">
        <DsfrTabContent panelId="tab-content-0" tabId="tab-0" :selected="selectedTabIndex === 0" :asc="asc">
          <IdentityTab :user="declarant" :company="company" />
        </DsfrTabContent>
        <DsfrTabContent panelId="tab-content-1" tabId="tab-1" :selected="selectedTabIndex === 1" :asc="asc">
          <SummaryTab v-model="declaration" />
        </DsfrTabContent>
        <DsfrTabContent panelId="tab-content-2" tabId="tab-2" :selected="selectedTabIndex === 2" :asc="asc">
          <HistoryTab />
        </DsfrTabContent>
        <DsfrTabContent panelId="tab-content-3" tabId="tab-3" :selected="selectedTabIndex === 3" :asc="asc">
          <DecisionTab />
        </DsfrTabContent>
      </DsfrTabs>
    </div>
  </div>
</template>

<script setup>
import { useRootStore } from "@/stores/root"
import { onMounted, computed, ref } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import SummaryTab from "./SummaryTab"
import IdentityTab from "./IdentityTab"
import HistoryTab from "./HistoryTab"
import DecisionTab from "./DecisionTab"

const store = useRootStore()
store.fetchDeclarationFieldsData()

const props = defineProps({
  declarationId: String,
})

const isDraft = computed(() => declaration.value?.status === "DRAFT")

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
  await executeDeclarantFetch()
  handleError(declarantResponse)
  await executeCompanyFetch()
  handleError(companyResponse)
  isFetching.value = false
})

// Tab management
const tabTitles = [
  { title: "Identité", icon: "ri-shield-user-line", tabId: "tab-0", panelId: "tab-content-0" },
  { title: "Le produit", icon: "ri-flask-line", tabId: "tab-1", panelId: "tab-content-1" },
  { title: "Historique", icon: "ri-chat-3-line", tabId: "tab-2", panelId: "tab-content-2" },
  { title: "Décision", icon: "ri-checkbox-circle-line", tabId: "tab-3", panelId: "tab-content-3" },
]
const selectedTabIndex = ref(0)
const asc = ref(true) // Je n'aime pas le nommage mais ça vient de ce paramètre : https://vue-dsfr.netlify.app/?path=/docs/composants-dsfrtabs--docs
const selectTab = (index) => {
  asc.value = selectedTabIndex.value < index
  selectedTabIndex.value = index
}
</script>
